import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();

    const upstream = await fetch(`${BACKEND_URL}/api/analyze`, {
      method: "POST",
      body: formData,
      cache: "no-store",
    });

    const text = await upstream.text();
    return new NextResponse(text, {
      status: upstream.status,
      headers: { "content-type": upstream.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return NextResponse.json(
      {
        detail:
          "Could not reach backend service. Start FastAPI on http://127.0.0.1:8000 or set BACKEND_URL in frontend/.env.local",
      },
      { status: 502 },
    );
  }
}
