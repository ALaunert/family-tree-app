<template>
  <main class="page-shell">
    <section class="panel">
      <h1>Sign in</h1>
      <p>Use your family tree account to continue.</p>

      <form class="form-stack" @submit.prevent="submit">
        <div class="field">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            autocomplete="email"
            name="email"
            required
            type="email"
          />
        </div>

        <div class="field">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            autocomplete="current-password"
            name="password"
            required
            type="password"
          />
        </div>

        <p v-if="error" class="error" role="alert">{{ error }}</p>

        <button class="button" :disabled="isSubmitting" type="submit">
          Sign in
        </button>
      </form>
    </section>
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { setCurrentUser, type SessionUser } from "../../app/session";
import { fetchJson } from "../../lib/fetchJson";

interface LoginResponse {
  user: SessionUser;
}

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      error: "",
      isSubmitting: false,
    };
  },
  methods: {
    async submit() {
      this.error = "";
      this.isSubmitting = true;

      try {
        const response = await fetchJson<LoginResponse>("/api/v1/auth/login", {
          method: "POST",
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        setCurrentUser(response.user);
        await this.$router.push(this.redirectTarget());
      } catch (error) {
        this.error = "Invalid email or password";
      } finally {
        this.isSubmitting = false;
      }
    },
    redirectTarget() {
      const redirect = this.$route?.query.redirect;
      if (typeof redirect === "string" && redirect.startsWith("/")) {
        return redirect;
      }

      return "/tree";
    },
  },
});
</script>
