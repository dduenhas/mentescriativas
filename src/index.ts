export interface Env {
  ASSETS: Fetcher;
  R2: R2Bucket;
}

const REDIRECTS: Record<string, string> = {
  "/blockly-aula-1": "/atividades/blockly-aula-1/",
  "/blockly-aula-2": "/atividades/blockly-aula-2/",
  "/blockly-games-aula-3": "/atividades/blockly-games-aula-3/",
  "/blockly-aula-4": "/atividades/blockly-aula-4/",
  "/microbit-aula-01": "/atividades/microbit-aula-01/",
  "/microbit-aula-02": "/atividades/microbit-aula-02/",
  "/microbit-aula-03": "/atividades/microbit-aula-03/",
  "/microbit-aula-04": "/atividades/microbit-aula-04/",
  "/scratchjr-aula-1": "/atividades/scratchjr-aula-1/",
  "/2025/10/222670-2": "/blog/bncc-competencias-e-habilidades/",
  "/project/blockly-games-sugestao-de-aulas":
    "/atividades/blockly-games-sugestao-de-aulas/",
};

const REDIRECT_PREFIXES: [RegExp, string][] = [
  [/^\/2025\/\d+\/(.+?)\/?$/, "/blog/$1/"],
  [
    /^\/(author|category|wpa-stats-type|layout_tag|layout_category)(\/.*)?$/,
    "/",
  ],
];

function normalizePath(pathname: string): string {
  let path = pathname;
  if (!path.startsWith("/")) path = `/${path}`;
  path = path.replace(/\/{2,}/g, "/");
  if (path.length > 1 && path.endsWith("/")) {
    return path.slice(0, -1);
  }
  return path;
}

function resolveRedirect(pathname: string): string | null {
  const path = normalizePath(pathname);

  if (REDIRECTS[path]) {
    return REDIRECTS[path];
  }

  for (const [pattern, target] of REDIRECT_PREFIXES) {
    const match = path.match(pattern);
    if (match) {
      return target.replace(/\$(\d+)/g, (_, n) => match[Number(n)] ?? "");
    }
  }

  return null;
}

function objectKeyFromPath(pathname: string): string {
  let path = pathname;
  if (path.startsWith("/")) path = path.slice(1);
  if (path.endsWith("/")) return `${path}index.html`;
  if (!path.includes(".")) return `${path}/index.html`;
  return path;
}

async function serveFromR2(
  request: Request,
  env: Env,
  key: string,
): Promise<Response | null> {
  if (key.includes("..")) {
    return new Response("Invalid path", { status: 400 });
  }

  const object = await env.R2.get(key);
  if (!object) return null;

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);
  headers.set("cache-control", "public, max-age=31536000, immutable");

  return new Response(object.body, { headers });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const redirect = resolveRedirect(url.pathname);
    if (redirect) {
      return Response.redirect(`${url.origin}${redirect}`, 301);
    }

    const staticResponse = await env.ASSETS.fetch(request);
    if (staticResponse.status !== 404) {
      return staticResponse;
    }

    const r2Key = objectKeyFromPath(url.pathname);
    const r2Response = await serveFromR2(request, env, r2Key);
    if (r2Response) {
      return r2Response;
    }

    return staticResponse;
  },
};
