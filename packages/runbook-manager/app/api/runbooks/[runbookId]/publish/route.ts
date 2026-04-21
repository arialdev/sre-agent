import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json(
    { error: "Runbook revisions are not supported" },
    { status: 405 },
  );
}
