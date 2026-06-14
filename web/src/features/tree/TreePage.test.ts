import { render, screen } from "@testing-library/vue";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import { defineComponent } from "vue";

import TreePage from "./TreePage.vue";

vi.mock("./components/FamilyTreeCanvas.vue", () => ({
  default: defineComponent({
    name: "FamilyTreeCanvasStub",
    props: {
      graph: {
        type: Object,
        required: true,
      },
    },
    emits: ["select-person"],
    template: `
      <div>
        <button
          v-for="node in graph.nodes.filter((candidate) => candidate.type === 'person')"
          :key="node.id"
          type="button"
          @click="$emit('select-person', node.data.person.id)"
        >
          {{ node.data.person.fullName }}
        </button>
      </div>
    `,
  }),
}));

describe("TreePage", () => {
  test("opens the details panel when a person node is selected", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ "content-type": "application/json" }),
        json: async () => ({
          viewerRole: "viewer",
          people: [
            {
              id: 1,
              fullName: "Ada Example",
              birthDate: "1815-12-10",
              deathDate: "1852-11-27",
              notes: "Tree Root",
            },
          ],
          relationships: [],
        }),
      }),
    );

    render(TreePage);

    await user.click(await screen.findByRole("button", { name: /ada example/i }));

    expect(screen.getByText(/tree root/i)).toBeInTheDocument();
  });
});
