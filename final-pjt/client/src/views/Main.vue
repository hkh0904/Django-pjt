<template>
  <div
    class="draggable"
    @mousedown="startDrag"
    @touchstart="startDrag"
    @mousemove="onDrag"
    @touchmove="onDrag"
    @mouseup="stopDrag"
    @touchend="stopDrag"
    @mouseleave="stopDrag"
  >
    <svg class="bg" width="100%" height="350">
      <path :d="headerPath" fill="#141414"></path>
    </svg>
    <div class="header">
      <kinesis-container>
        <kinesis-element :strength="10" :class="{ zoomin: showHeader }">
          What page is it?
        </kinesis-element>
        <kinesis-element :strength="20">
          This is shows the preferences of new subscribers. <br />
          Aren't you curious, right? <br />
          Then hold this header and stretch it out! As much as you want
          <br /><br /><br />
          <kinesis-element
            :strength="20"
            v-if="showCheckIcon"
            style="color: #abd6ac"
          >
            Please click the button below
          </kinesis-element>
          <kinesis-element :strength="20" v-else style="color: white">
            Please click the button below
          </kinesis-element>
        </kinesis-element>
      </kinesis-container>
    </div>
    <div class="body-box" :class="{ 'bg-success': showCheckIcon }">
      <div style="height: 250px"></div>
      <button
        @click="toggleText"
        style="
          border: none;
          background-color: #abd6ac;
          border-radius: 25px;
          height: 50px;
          width: 50px;
          font-size: 25px;
        "
      >
        📌
      </button>
      <div :class="{ zoomin: showText, zoomout: !showText }">
        <div>
          <div class="main-box">
            <div class="poster-box">
              <div>
                <br />
                <h1 style="color: dimgray; text-align: left; margin-left: 0%">
                  Choice!
                </h1>
                <h5 style="text-align: left; color: dimgray">
                  Configure the recommended algorithm based on your selection.
                </h5>
                <hr />
              </div>
              <div class="container1">
                <div class="row row-cols-xxl-3 g-10">
                  <div class="col1" v-for="(movie, idx) in URL" :key="idx">
                    <div class="image-container">
                      <img
                        :src="movie"
                        style="width: 100%"
                        class="image"
                        @click="toggleImageShadow(idx)"
                        :class="{ shadow: isImageClicked.includes(idx) }"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <b-button
            variant="outline-success"
            @click="showSecondButton = true"
            v-if="!showSecondButton"
          >
            Submit
          </b-button>
          <b-button
            variant="outline-danger"
            v-else-if="showSecondButton && !showCheckIcon"
            @click="showCheckIcon = true"
          >
            Check
          </b-button>
          <button
            v-if="showCheckIcon"
            style="
              color: white;
              border: none;
              width: 50px;
              background-color: #95bc96;
              border-radius: 25px;
              font-size: 30px;
            "
            @click="[show_modal(), (showModal = true)]"
          >
            ✔
          </button>
          <b-modal
            v-model="showModal"
            title="Modal Title"
            @hidden="handleModalHidden"
          >
            <h4>선택하신 영화가 맞으신가요?</h4>
            <p>맞으시면 확인버튼을 눌러주세요</p>
            <br />
            <ul v-for="(idx, i) in show_title" :key="idx">
              <li>
                {{ show_title[i] }}
              </li>
            </ul>
            <template #modal-footer="{ ok, cancel }">
              <b-button variant="danger" type="button" @click="cancel()"
                >닫기</b-button
              >
              <router-link :to="{ name: 'home' }">
                <b-button variant="success" @click="ok()">확인</b-button>
              </router-link>
            </template>
          </b-modal>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script setup>
import store from "@/store";
import { ref, reactive, computed, onMounted } from "vue";
import { KinesisContainer, KinesisElement } from "vue-kinesis";
import dynamics from "dynamics.js";
import vueConfirmationButton from "vue-confirmation-button";
import Vue from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/GoonManDu";

const headerHeight = 250; // 높이 조절

const URL = ref([]);
const genres = [];

axios
  .get(`${API_URL}/movies/`)
  .then((res) => {
    const tmp = [];
    const genre = [];
    for (let i = 0; i < 80; i++) {
      // console.log(res.data)
      tmp.push("https://image.tmdb.org/t/p/w500" + res.data[i].poster_path);
      genres.push([res.data[i].title, res.data[i].genre_ids]);
    }
    URL.value = tmp;
  })
  .catch((err) => {
    console.log(err);
  });

let isDragging = false;
const start = { x: 0, y: 0 };
const c = reactive({ x: headerHeight, y: headerHeight });
const showText = ref(false);
const showSecondButton = ref(false);
const showCheckIcon = ref(false);
const showHeader = ref(true);
const showModal = ref(false);
const isImageClicked = Vue.observable([]);
const isImageRotated = Vue.observable([]);

// Set으로 변경

const headerPath = computed(() => {
  return `M0,0 L4640,0 4640,${headerHeight}Q${c.x},${c.y} 0,${headerHeight}`;
});

const contentPosition = computed(() => {
  const dy = c.y - headerHeight;
  const dampen = dy > 0 ? 2 : 4;
  return {
    transform: `translate(0,${dy / dampen}px)`,
  };
});

function startDrag(e) {
  e = e.changedTouches ? e.changedTouches[0] : e;
  isDragging = true;
  start.x = e.pageX;
  start.y = e.pageY;
}

function onDrag(e) {
  e = e.changedTouches ? e.changedTouches[0] : e;
  if (isDragging) {
    c.x = headerHeight + (e.pageX - start.x);
    const dy = e.pageY - start.y;
    const dampen = dy > 0 ? 1.5 : 4;
    c.y = headerHeight + dy / dampen;
  }
}

function stopDrag() {
  if (isDragging) {
    isDragging = false;
    dynamics.animate(
      c,
      { x: headerHeight, y: headerHeight },
      { type: dynamics.spring, duration: 700, friction: 280 }
    );
  }
}

function toggleText() {
  if (showText.value) {
    dynamics.animate(
      document.querySelector(".zoomin"),
      { opacity: 0, translateX: -100 },
      {
        type: dynamics.easeInOut,
        duration: 500,
        complete: () => {
          showText.value = !showText.value;
        },
      }
    );
  } else {
    showText.value = !showText.value;
    setTimeout(() => {
      dynamics.animate(
        document.querySelector(".zoomin"),
        { opacity: 1, translateX: 0 },
        {
          type: dynamics.easeInOut,
          duration: 500,
        }
      );
    }, 0);
  }
}

function toggleImageShadow(index) {
  if (isImageClicked.includes(index)) {
    isImageClicked.splice(isImageClicked.indexOf(index), 1); // 이미 클릭된 이미지면 제거
  } else {
    isImageClicked.push(index); // 클릭된 이미지가 아니면 추가
  }
  if (isImageRotated.includes(index)) {
    isImageRotated.splice(isImageRotated.indexOf(index), 1); // 이미 회전된 이미지면 제거
  } else {
    isImageRotated.push(index); // 회전되지 않은 이미지면 추가
  }
}
var show_title = [];
var show_genres = [];

function show_modal() {
  for (var i = 0; i < isImageClicked.length; i++) {
    // console.log(genres[isImageClicked[i]][1]);
    show_title.push(genres[isImageClicked[i]][0]);
    show_genres.push(genres[isImageClicked[i]][1]);
  }
  store.commit("REC_GENRES", show_genres);
  // console.log(show_genres);
}

function handleModalHidden() {
  // 모달이 닫힐 때 실행되는 로직
  location.reload(); // 페이지 새로고침
}
</script>

<style scoped>
#app {
  height: auto;
}
.draggable {
  background-color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  width: 100%;
  height: 50%;
  overflow: hidden;
  margin: 30px auto;
  position: relative;
  text-align: center;
  font-size: 14px;
  font-weight: 300;
  user-select: none;
  border-radius: 0px 0px 8px 8px;
}
.bg {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
}
.header {
  color: #fff;
  height: 120px;
  font-size: 2em;
  font-weight: bold;
  top: 150px; /* Adjust the value here to move the black bar down */
}
.content {
  position: relative;
  z-index: 1;
  padding: 30px;
  box-sizing: border-box;
}
.header {
  color: #fff;
  height: 120px;
  font-size: 2em;
  font-weight: bold;
}

.zoomin {
  height: auto;
  font-size: 2em;
  font-weight: bold;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 0;
  transform: translateX(100%);
  animation-name: zoomInRight;
}

.zoomout {
  height: 120px;
  font-size: 2em;
  font-weight: bold;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 1;
  transform: translateX(-100%);
  animation-name: zoomOutLeft;
}

@keyframes zoomInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes zoomOutLeft {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-100%);
  }
}

.body-box {
  background-color: white;
  height: auto;
  padding-bottom: 50px;
}

.bg-success {
  background-color: #abd6ac !important;
}

.main-box {
  width: 90%;
  height: auto;
  margin: auto;
  padding-bottom: 40px;
}

.container1 {
  height: auto;
  padding-top: 2%;
  overflow: hidden;
}

.col1 {
  width: 12%;
  margin-bottom: 30px;
  padding: 0 8px;
  cursor: pointer;
  transition: box-shadow 0.3s ease; /* Add transition effect for the shadow */
}

.image-container:hover {
  box-shadow: 0 48px 48px rgba(0, 0, 0, 0.8);
  z-index: 1;
}

.image-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.image-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  height: 100%;
}

.shadow {
  /* box-shadow: 0px 8px 0px 4px rgba(157, 255, 0, 0.4) !important; */
  transform: rotateZ(360deg);
  transition: transform 1s;
  z-index: 2;
  opacity: 0.25;
}
</style>
