import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "https://agentic-lead-engine.onrender.com";
const API_KEY = process.env.BACKEND_API_KEY || "changeme";

export async function GET(req: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path.join("/");
  const url = new URL(`/api/${path}`, BACKEND_URL);
  url.search = req.nextUrl.searchParams.toString();
  try {
    const res = await fetch(url.toString(), {
      headers: { "X-API-KEY": API_KEY },
    });
    const body = await res.text();
    return new NextResponse(body, { status: res.status, headers: { "Content-Type": "application/json" } });
  } catch (e) {
    return NextResponse.json({ error: "Backend unreachable", details: String(e) }, { status: 502 });
  }
}

export async function POST(req: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path.join("/");
  const url = new URL(`/api/${path}`, BACKEND_URL);
  try {
    const body = await req.text();
    const res = await fetch(url.toString(), {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-API-KEY": API_KEY },
      body,
    });
    const data = await res.text();
    return new NextResponse(data, { status: res.status, headers: { "Content-Type": "application/json" } });
  } catch (e) {
    return NextResponse.json({ error: "Backend unreachable", details: String(e) }, { status: 502 });
  }
}

export async function PATCH(req: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path.join("/");
  const url = new URL(`/api/${path}`, BACKEND_URL);
  try {
    const body = await req.text();
    const res = await fetch(url.toString(), {
      method: "PATCH",
      headers: { "Content-Type": "application/json", "X-API-KEY": API_KEY },
      body,
    });
    const data = await res.text();
    return new NextResponse(data, { status: res.status, headers: { "Content-Type": "application/json" } });
  } catch (e) {
    return NextResponse.json({ error: "Backend unreachable", details: String(e) }, { status: 502 });
  }
}