import { fetchJson } from "../../lib/fetchJson";
import type { TreeDto } from "./types";

export function fetchTree(): Promise<TreeDto> {
  return fetchJson<TreeDto>("/api/v1/tree");
}
