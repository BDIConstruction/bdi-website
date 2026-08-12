/**
 * Sign-in for the site admin at /admin.
 *
 * GitHub Pages only serves files, so it cannot finish an OAuth sign-in on its
 * own: the last step trades a temporary code for an access token, and that
 * trade needs the client secret. A secret cannot live in a web page, where
 * anyone could read it. This worker is the only place that holds it.
 *
 * Two routes:
 *   /auth      starts the flow and sends the browser to GitHub
 *   /callback  GitHub returns here; swaps the code for a token and hands it
 *              back to the admin window that opened the popup
 *
 * Set these in the Cloudflare dashboard, under Settings -> Variables:
 *   GITHUB_CLIENT_ID      from the OAuth App                    (secret)
 *   GITHUB_CLIENT_SECRET  from the OAuth App                    (secret)
 *   ALLOWED_ORIGIN        https://bdiconstruction.github.io     (plain text)
 *   SCOPE                 optional; defaults to public_repo
 */

const AUTHORIZE_URL = "https://github.com/login/oauth/authorize";
const TOKEN_URL = "https://github.com/login/oauth/access_token";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/auth") return startSignIn(env, url);
    if (url.pathname === "/callback") return finishSignIn(request, env, url);
    return new Response("Not found", { status: 404 });
  },
};

function startSignIn(env, url) {
  // A random value that GitHub echoes back, so a callback which did not
  // begin here can be told apart from one that did and rejected.
  const state = crypto.randomUUID();

  const target = new URL(AUTHORIZE_URL);
  target.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  target.searchParams.set("redirect_uri", `${url.origin}/callback`);
  target.searchParams.set("scope", env.SCOPE || "public_repo");
  target.searchParams.set("state", state);

  return new Response(null, {
    status: 302,
    headers: {
      Location: target.toString(),
      "Set-Cookie":
        `oauth_state=${state}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=600`,
    },
  });
}

async function finishSignIn(request, env, url) {
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  const cookie = (request.headers.get("Cookie") || "")
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith("oauth_state="));
  const expected = cookie ? cookie.slice("oauth_state=".length) : null;

  if (!code || !state || !expected || state !== expected) {
    return handshake(env, { error: "The sign-in could not be verified. Please try again." });
  }

  const response = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: `${url.origin}/callback`,
    }),
  });

  const data = await response.json();
  if (!data.access_token) {
    return handshake(env, { error: data.error_description || "GitHub declined the sign-in." });
  }
  return handshake(env, { token: data.access_token });
}

/**
 * The admin page opened this popup and is waiting to be spoken to. It says
 * hello first, and only then is the token passed back — and only ever to the
 * one origin the site is served from, never to whoever happens to be
 * listening.
 */
function handshake(env, result) {
  const origin = env.ALLOWED_ORIGIN;
  const message = result.token
    ? `authorization:github:success:${JSON.stringify({ token: result.token, provider: "github" })}`
    : `authorization:github:error:${JSON.stringify({ message: result.error })}`;

  const body = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Signing in</title></head>
<body style="font:15px/1.6 system-ui,sans-serif;padding:2rem;color:#15202B">
${result.token ? "Signing you in&hellip;" : "Sign-in failed. You can close this window."}
<script>
(function () {
  var origin  = ${JSON.stringify(origin)};
  var message = ${JSON.stringify(message)};
  function reply(event) {
    if (event.origin !== origin) return;   // never answer anyone else
    window.opener.postMessage(message, origin);
    window.removeEventListener("message", reply, false);
  }
  window.addEventListener("message", reply, false);
  window.opener.postMessage("authorizing:github", origin);
})();
</script>
</body></html>`;

  return new Response(body, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      // the state cookie has done its job
      "Set-Cookie": "oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0",
    },
  });
}
