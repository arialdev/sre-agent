import { NextResponse } from "next/server";

import { getRunbookServices } from "@/src/lib/runbooks/container";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ runbookId: string }> },
) {
  const { runbookId } = await params;
  const services = getRunbookServices();
  const detail = await services.management.getRunbookDetail(runbookId);

  if (!detail) {
    return NextResponse.json({ error: "Runbook not found" }, { status: 404 });
  }

  return NextResponse.json({ detail });
}

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ runbookId: string }> },
) {
  const { runbookId } = await params;
  const body = (await request.json()) as { confirmationSlug?: string };
  const services = getRunbookServices();
  const runbook = await services.management.getRunbook(runbookId);

  if (!runbook) {
    return NextResponse.json({ error: "Runbook not found" }, { status: 404 });
  }

  if (body.confirmationSlug !== runbook.slug) {
    return NextResponse.json(
      { error: "Runbook slug confirmation does not match" },
      { status: 400 },
    );
  }

  await services.management.deleteRunbook(runbookId);
  return NextResponse.json({ ok: true });
}
