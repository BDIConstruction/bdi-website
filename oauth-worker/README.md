# Admin sign-in worker

`worker.js` is the sign-in service for the admin at `/admin`. It is not part
of the website and is never served with it — it runs on Cloudflare Workers.

## Why it exists

GitHub Pages only serves files. Signing in with GitHub ends with trading a
temporary code for an access token, and that trade needs the OAuth App's
client secret. A secret cannot sit in a web page where any visitor could read
it, so something has to hold it off to one side. That is all this does.

Netlify Identity used to play this part.

## Deploying it

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Create Worker**
2. Name it `bdi-cms-auth`, deploy the placeholder it gives you
3. **Edit code**, replace everything with `worker.js`, deploy
4. **Settings → Variables and Secrets**, add:

   | Name | Type | Value |
   |---|---|---|
   | `GITHUB_CLIENT_ID` | Secret | from the OAuth App |
   | `GITHUB_CLIENT_SECRET` | Secret | from the OAuth App |
   | `ALLOWED_ORIGIN` | Text | `https://bdiconstruction.github.io` |

   `ALLOWED_ORIGIN` takes a comma-separated list, so during a move to a new
   domain both addresses can be served at once:
   `https://bdiconstruction.github.io, https://bdiconstruction.com`.
   A trailing slash or a path is tolerated — each entry is reduced to its
   origin — but an unrelated origin is never accepted.

5. Copy the worker's address, then set the OAuth App's **Authorization
   callback URL** to that address with `/callback` on the end

`SCOPE` may also be set; it defaults to `public_repo`, which is enough while
this repository is public. A private repository needs `repo`.

## What it does

| Route | |
|---|---|
| `/auth` | starts the flow, hands the browser to GitHub |
| `/callback` | GitHub returns here; swaps the code for a token and passes it back to the admin window |

The token goes only to `ALLOWED_ORIGIN` and only after that window has spoken
first. A random `state` value is carried through the round trip in a cookie,
so a callback that did not begin at `/auth` is refused.
