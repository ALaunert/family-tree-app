<template>
  <aside class="details-panel" aria-label="Person details">
    <button class="close-button" type="button" aria-label="Close details" @click="$emit('close')">
      x
    </button>
    <h2>{{ person.fullName }}</h2>
    <button
      v-if="canEdit"
      class="edit-button"
      type="button"
      @click="$emit('edit', person.id)"
    >
      Edit person
    </button>
    <dl>
      <div v-if="person.birthDate">
        <dt>Born</dt>
        <dd>{{ person.birthDate }}</dd>
      </div>
      <div v-if="person.deathDate">
        <dt>Died</dt>
        <dd>{{ person.deathDate }}</dd>
      </div>
    </dl>
    <p v-if="person.notes" class="notes">{{ person.notes }}</p>

    <section v-if="partners.length">
      <h3>Partners</h3>
      <ul>
        <li v-for="partner in partners" :key="partner.id">{{ partner.fullName }}</li>
      </ul>
    </section>

    <section v-if="parents.length">
      <h3>Parents</h3>
      <ul>
        <li v-for="parent in parents" :key="parent.id">{{ parent.fullName }}</li>
      </ul>
    </section>

    <section v-if="children.length">
      <h3>Children</h3>
      <ul>
        <li v-for="child in children" :key="child.id">{{ child.fullName }}</li>
      </ul>
    </section>
  </aside>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

import type { PersonDto, RelationshipDto } from "../tree/types";

export default defineComponent({
  name: "PersonDetailsPanel",
  props: {
    person: {
      type: Object as PropType<PersonDto>,
      required: true,
    },
    people: {
      type: Array as PropType<PersonDto[]>,
      required: true,
    },
    relationships: {
      type: Array as PropType<RelationshipDto[]>,
      required: true,
    },
    canEdit: {
      type: Boolean,
      default: false,
    },
  },
  emits: {
    close: () => true,
    edit: (personId: number) => Number.isInteger(personId),
  },
  computed: {
    peopleById(): Map<number, PersonDto> {
      return new Map(this.people.map((person) => [person.id, person]));
    },
    partners(): PersonDto[] {
      return this.relationships
        .filter(
          (relationship) =>
            relationship.type === "partner" &&
            (relationship.sourcePersonId === this.person.id ||
              relationship.targetPersonId === this.person.id),
        )
        .map((relationship) =>
          relationship.sourcePersonId === this.person.id
            ? this.peopleById.get(relationship.targetPersonId)
            : this.peopleById.get(relationship.sourcePersonId),
        )
        .filter((person): person is PersonDto => person !== undefined);
    },
    parents(): PersonDto[] {
      return this.relationships
        .filter(
          (relationship) =>
            relationship.type === "parent_child" &&
            relationship.targetPersonId === this.person.id,
        )
        .map((relationship) => this.peopleById.get(relationship.sourcePersonId))
        .filter((person): person is PersonDto => person !== undefined);
    },
    children(): PersonDto[] {
      return this.relationships
        .filter(
          (relationship) =>
            relationship.type === "parent_child" &&
            relationship.sourcePersonId === this.person.id,
        )
        .map((relationship) => this.peopleById.get(relationship.targetPersonId))
        .filter((person): person is PersonDto => person !== undefined);
    },
  },
});
</script>

<style scoped>
.details-panel {
  position: relative;
  display: grid;
  align-content: start;
  gap: 16px;
  min-width: 280px;
  padding: 24px;
  border-left: 1px solid #d9e2ec;
  background: #ffffff;
}

.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 34px;
  height: 34px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  background: #ffffff;
  cursor: pointer;
}

h2,
h3,
p,
dl,
ul {
  margin: 0;
}

h2 {
  padding-right: 36px;
  font-size: 1.35rem;
  line-height: 1.2;
}

.edit-button {
  width: max-content;
  min-height: 38px;
  padding: 0 12px;
  border: 1px solid #1f2933;
  border-radius: 6px;
  background: #ffffff;
  color: #1f2933;
  font-weight: 700;
  cursor: pointer;
}

h3 {
  margin-bottom: 8px;
  font-size: 0.92rem;
  text-transform: uppercase;
  letter-spacing: 0;
  color: #52606d;
}

dl {
  display: grid;
  gap: 8px;
}

dt {
  color: #52606d;
  font-size: 0.86rem;
}

dd {
  margin: 0;
  font-weight: 600;
}

ul {
  display: grid;
  gap: 6px;
  padding-left: 18px;
}

.notes {
  color: #334e68;
  line-height: 1.5;
}
</style>
