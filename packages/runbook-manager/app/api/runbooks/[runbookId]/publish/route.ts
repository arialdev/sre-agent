import { NextResponse } from "next/server";

import { getRunbookServices } from "@/src/lib/runbooks/container";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ runbookId: string }> },
) {
  const { runbookId } = await params;
  const body = (await request.json()) as { versionId?: string };
  const versionId = body.versionId;

  if (!versionId) {
    return NextResponse.json(
      { error: "versionId is required" },
      { status: 400 },
    );
  }

  const services = getRunbookServices();
  const runbook = await services.management.publishVersion(runbookId, versionId);
  return NextResponse.json({ runbook });
}
