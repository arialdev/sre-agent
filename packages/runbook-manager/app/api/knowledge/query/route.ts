import { NextResponse } from "next/server";

import { getRunbookServices } from "@/src/lib/runbooks/container";
import { parseKnowledgeQuery } from "@/src/lib/runbooks/input";

export async function POST(request: Request) {
  const body = await request.json();
  const input = parseKnowledgeQuery(body);
  const services = getRunbookServices();
  const results = await services.retrieval.query(input);

  return NextResponse.json({
    query: input.query,
    results,
  });
}
