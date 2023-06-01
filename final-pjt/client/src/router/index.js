import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/movies/HomeView.vue";
import MovieDetail from "../views/movies/MovieDetail.vue";
import ArticleDetail from "../views/articles/ArticleDetailView.vue";
import ExploreAll from "../views/movies/ExploreAll.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "main",
    component: () => import("../views/Main.vue"),
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/movies/AboutView.vue"),
  },
  {
    path: "/recommended",
    name: "recommended",
    component: () => import("../views/movies/RecommendedView.vue"),
  },
  {
    path: "/articles",
    name: "articles",
    component: () => import("../views/articles/ArticlesList.vue"),
  },
  {
    path: "/my/profile",
    name: "myprofile",
    component: () => import("../views/accounts/MyProfileView.vue"),
  },
  {
    path: "/:account_id/profile",
    name: "profile",
    component: () => import("../views/accounts/ProfileView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/accounts/SignupView.vue"),
  },
  {
    path: "/userUpdate",
    name: "userUpdate",
    component: () => import("../views/accounts/UpdateProfileView.vue"),
  },
  {
    path: "/exploreall/:name",
    name: "exploreall",
    component: ExploreAll,
    beforeEnter: (to, from, next) => {
      return next();
    },
  },
  {
    path: "/article/:article_id",
    name: "article_detail",
    component: ArticleDetail,
  },
  {
    path: "/article/:article_id/update",
    name: "article_update",
    component: () => import("../views/articles/UpdateArticleView.vue"),
  },
  {
    path: "/movie/:movie_id",
    name: "movie_detail",
    component: MovieDetail,
    beforeEnter: (to, from, next) => {
      return next();
    },
  },
  {
    path: "/searchMovie/",
    name: "searchMovie",
    component: () => import("../views/movies/SearchMovieView.vue")
  },
  {
    path: "/movie/:movie_id/videos",
    name: "movie_detail_videos",
    component: () => import("../views/movies/details/MovieDetailVideos.vue"),
  },
  {
    path: "/movie/:movie_id/photos",
    name: "movie_detail_photos",
    component: () => import("../views/movies/details/MovieDetailPhotos.vue"),
  },
  {
    path: "/movie/:movie_id/comment",
    name: "movie_detail_comment",
    component: () => import("../views/movies/details/MovieDetailComment.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
