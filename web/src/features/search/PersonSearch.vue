<template>
  <form class="person-search" role="search" @submit.prevent>
    <label for="person-search-input">Quick jump</label>
    <input
      id="person-search-input"
      v-model="searchText"
      type="search"
      autocomplete="off"
      placeholder="Find a person"
    />
    <div v-if="searchText.trim() && filteredPeople.length" class="search-results">
      <button
        v-for="person in filteredPeople"
        :key="person.id"
        type="button"
        @click="$emit('select-person', person.id)"
      >
        {{ person.fullName }}
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

import type { PersonDto } from "../tree/types";

export default defineComponent({
  name: "PersonSearch",
  props: {
    people: {
      type: Array as PropType<PersonDto[]>,
      required: true,
    },
  },
  emits: {
    "select-person": (personId: number) => Number.isInteger(personId),
  },
  data() {
    return {
      searchText: "",
    };
  },
  computed: {
    filteredPeople(): PersonDto[] {
      const query = this.searchText.trim().toLocaleLowerCase();

      if (!query) {
        return this.people;
      }

      return this.people.filter((person) =>
        person.fullName.toLocaleLowerCase().includes(query),
      );
    },
  },
});
</script>

<style scoped>
.person-search {
  display: grid;
  gap: 8px;
  width: min(100%, 320px);
}

label {
  color: #52606d;
  font-size: 0.86rem;
  font-weight: 700;
}

input {
  width: 100%;
  min-height: 40px;
  padding: 9px 12px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  background: #ffffff;
}

input:focus {
  border-color: #2f80ed;
  outline: 3px solid rgb(47 128 237 / 18%);
}

.search-results {
  display: grid;
  max-height: 180px;
  overflow: auto;
  border: 1px solid #d9e2ec;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 10px 24px rgb(16 24 40 / 8%);
}

.search-results button {
  min-height: 38px;
  padding: 8px 10px;
  border: 0;
  border-bottom: 1px solid #edf2f7;
  background: #ffffff;
  color: #1f2933;
  text-align: left;
  cursor: pointer;
}

.search-results button:last-child {
  border-bottom: 0;
}

.search-results button:hover,
.search-results button:focus {
  background: #f0f4f8;
  outline: none;
}
</style>
