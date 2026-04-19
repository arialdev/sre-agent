import { NextResponse } from "next/server";

import { getRunbookServices } from "@/src/lib/runbooks/container";
import { parseRunbookMutationFormData } from "@/src/lib/runbooks/input";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ runbookId: string }> },
) {
  const { runbookId } = await params;
  const formData = await request.formData();
  const input = await parseRunbookMutationFormData(formData);
  const services = getRunbookServices();
  const version = await services.management.createVersion(runbookId, input);
  return NextResponse.json({ version }, { status: 201 });
}
