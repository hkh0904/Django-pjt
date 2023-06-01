<template>
  <div>
    <h1>수정</h1>
    <p>{{ article_id }}</p>
    <p>{{ article_info }}</p>
    <b-input v-model="update_title"></b-input>
    <b-input v-model="update_content"></b-input>
    <b-button @click="cancle(article_id)">취소</b-button>
    <b-button variant="primary" @click="updateArticle(article_id)"
      >수정</b-button
    >
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";
export default {
  name: "updateArticle",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      article_id: null,
      article_info: null,
      update_title: null,
      update_content: null,
    };
  },
  created() {
    this.article_id = this.$route.params.article_id;
    this.getArticle();
  },
  methods: {
    getArticle() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/${this.article_id}`,
      })
        .then((response) => {
          this.article_info = response.data;
          this.update_title = response.data.title;
          this.update_content = response.data.content;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    cancle(article_id) {
      this.$router.push({
        name: "article_detail",
        params: { article_id: article_id },
      });
    },
    updateArticle(article_id) {
      const user = this.article_info.user
      const title = this.update_title;
      const content = this.update_content;

      console.log(user, title, content)

      axios({
        method: "put",
        url: `${API_URL}/articles/${article_id}/`,
        data: {
          user, title, content,
        },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          this.$router.push({
            name: "article_detail",
            params: { article_id: this.article_id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
