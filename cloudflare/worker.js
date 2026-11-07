// GLOBAL PETRO — static site + one endpoint that e-mails form enquiries to the company (via Resend).
// Secret: RESEND_API_KEY (wrangler secret put RESEND_API_KEY). Static files are served from ./public.

const CANONICAL_HOST = "globalpetro.cz";
const TO = "email.global.petro@seznam.cz";
const FROM = "GLOBAL PETRO web <poptavka@globalpetro.cz>";
const ALLOWED_ORIGINS = ["https://globalpetro.cz", "https://www.globalpetro.cz", "https://global-petro.kolato90.workers.dev"];
const LIMITS = { name: 120, phone: 40, email: 160, object_type: 80, message: 3000 };
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function json(status, body) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8" } });
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

/** Returns the cleaned enquiry or an error message for the visitor. */
export function validate(input) {
  if (!input || typeof input !== "object") return { error: "Neplatná data." };
  const clean = {};
  for (const [key, max] of Object.entries(LIMITS)) {
    const value = typeof input[key] === "string" ? input[key].trim() : "";
    if (value.length > max) return { error: "Text je příliš dlouhý." };
    clean[key] = value;
  }
  if (!clean.name || !clean.phone || !clean.message) return { error: "Vyplňte jméno, telefon a zprávu." };
  if (clean.email && !EMAIL_RE.test(clean.email)) return { error: "Zkontrolujte e-mail." };
  return { value: clean };
}

function buildEmail(e) {
  const rows = [
    ["Jméno / firma", e.name],
    ["Telefon", e.phone],
    ["E-mail", e.email || "—"],
    ["Obor", e.object_type || "—"],
  ];
  const text = rows.map(([k, v]) => `${k}: ${v}`).join("\n") + `\n\n${e.message}\n\n— odesláno z webu globalpetro.cz`;
  const html =
    `<table style="font:15px/1.5 Arial,sans-serif;border-collapse:collapse">` +
    rows.map(([k, v]) => `<tr><td style="padding:4px 16px 4px 0;color:#666">${k}</td><td style="padding:4px 0"><b>${escapeHtml(v)}</b></td></tr>`).join("") +
    `</table><p style="font:15px/1.6 Arial,sans-serif;white-space:pre-wrap">${escapeHtml(e.message)}</p>` +
    `<p style="font:12px Arial,sans-serif;color:#999">Odesláno z webu globalpetro.cz</p>`;
  return {
    from: FROM,
    to: [TO],
    reply_to: e.email || undefined,
    subject: `Poptávka pracovníků — ${e.object_type || "web"} — ${e.name}`.slice(0, 180),
    text,
    html,
  };
}

async function handleEnquiry(request, env) {
  const origin = request.headers.get("origin");
  if (origin && !ALLOWED_ORIGINS.includes(origin)) return json(403, { ok: false, error: "Nepovolený zdroj." });
  if (!(request.headers.get("content-type") || "").includes("application/json")) return json(415, { ok: false, error: "Neplatná data." });

  let input;
  try {
    input = await request.json();
  } catch {
    return json(400, { ok: false, error: "Neplatná data." });
  }
  // Honeypot: people never see this field, bots fill it. Pretend success so they do not retry.
  if (typeof input?.website === "string" && input.website.trim()) return json(200, { ok: true });

  const { value, error } = validate(input);
  if (error) return json(400, { ok: false, error });
  if (!env.RESEND_API_KEY) {
    console.error("enquiry: RESEND_API_KEY is not set");
    return json(503, { ok: false, error: "Odeslání není k dispozici." });
  }

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify(buildEmail(value)),
  });
  if (!res.ok) {
    console.error("enquiry: resend failed", res.status, await res.text());
    return json(502, { ok: false, error: "Odeslání se nezdařilo." });
  }
  return json(200, { ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // One address for search engines: www and workers.dev permanently redirect to the main domain.
    if (url.hostname !== CANONICAL_HOST) {
      return Response.redirect(`https://${CANONICAL_HOST}${url.pathname}${url.search}`, 301);
    }
    if (url.pathname === "/api/poptavka") {
      if (request.method !== "POST") return json(405, { ok: false, error: "Method not allowed" });
      return handleEnquiry(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};
