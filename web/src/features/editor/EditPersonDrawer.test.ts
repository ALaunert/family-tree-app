import { render, screen } from "@testing-library/vue";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import { defineComponent } from "vue";

import PersonSearch from "../search/PersonSearch.vue";
import type { PersonDto, TreeDto } from "../tree/types";
import TreePage from "../tree/TreePage.vue";

vi.mock("../tree/components/FamilyTreeCanvas.vue", () => ({
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

const peopleFixture: PersonDto[] = [
  {
    id: 1,
    fullName: "Ada Example",
    birthDate: "1815-12-10",
    deathDate: "1852-11-27",
    notes: "Tree Root",
  },
  {
    id: 2,
    fullName: "Grace Hopper",
    birthDate: null,
    deathDate: null,
    notes: null,
  },
];

function stubTree(tree: TreeDto) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => tree,
    }),
  );
}

describe("moderator editing tools", () => {
  test("shows moderator controls only for moderator sessions", async () => {
    stubTree({
      viewerRole: "viewer",
      people: peopleFixture,
      relationships: [],
    });

    const { unmount } = render(TreePage);

    await screen.findByRole("button", { name: /ada example/i });

    expect(screen.queryByRole("button", { name: /add person/i })).not.toBeInTheDocument();

    unmount();

    stubTree({
      viewerRole: "moderator",
      people: peopleFixture,
      relationships: [],
    });

    render(TreePage);

    expect(await screen.findByRole("button", { name: /add person/i })).toBeVisible();
  });

  test("filters the quick-jump list by deferred search text", async () => {
    const user = userEvent.setup();

    render(PersonSearch, { props: { people: peopleFixture } });

    await user.type(screen.getByRole("searchbox"), "ada");

    expect(screen.getByRole("button", { name: /ada example/i })).toBeVisible();
    expect(screen.queryByRole("button", { name: /grace hopper/i })).not.toBeInTheDocument();
  });
});
