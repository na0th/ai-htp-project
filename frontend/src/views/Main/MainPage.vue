<template>
  <div v-if="showMain" class="main">
    <div class="title">
      <img class="title-image" src="../../assets/images/icon5.png" />
      <p class="title-text"><span style="color: #eba090">마음</span>스케치</p>
      <p class="title-subtext">내가 그린 그림으로 확인해보는 나의 심리</p>
    </div>
    <button
      type="button"
      @click="toggleMain"
      @ToFirstScene="$emit('ToFirstScene')"
      class="start-btn"
    >
      START
    </button>
  </div>

  <transition name="main">
    <PreStartPage
      v-bind:isPlaying="isPlaying"
      @ToFirstScene="ToFirstScene"
      @toggleSound="toggleSound"
      v-if="showPre"
    ></PreStartPage>
  </transition>
</template>

<script>
import PreStartPage from "./PreStartPage.vue";
export default {
  name: "MainPage",
  components: { PreStartPage },
  props: ["isPlaying"],
  data() {
    return {
      current: {},
      index: 0,
      showMain: true,
      showPre: false,
      sounds: [
        {
          title: "MainSound",
          src: require("../../assets/audio/start.mp3"),
        },
      ],
      player: new Audio(),
    };
  },
  created() {
    this.current = this.sounds[this.index];
    this.player.src = this.current.src;
  },
  methods: {
    ToFirstScene() {
      this.$emit("ToFirstScene");
    },
    toggleMain() {
      this.player.play();
      this.showMain = !this.showMain;
      this.showPre = !this.showPre;
    },
    toggleSound() {
      this.$emit("toggleSound");
    },
  },
  setup() {
    const setScreenSize = function () {
      let vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`); //핸드폰 화면에 맞게 vh 새로 설정
    };
    setScreenSize();
    window.addEventListener("resize", () => setScreenSize());
  },
};
</script>

<style>
.main {
  background-image: url("../../assets/images/mainPage.png");
  height: calc(var(--vh, 1vh) * 100);
  color: #3c3c3c;
  overflow: hidden;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
}
.title {
  text-align: left;
  display: inline-block;
  padding-right: 20px;
  font-size: 42px;
  font-family: korFont1;
  margin-top: 50px;
  font-weight: 1000;
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
  text-align: center;
  top: 28%;
}
.title-image {
  width: 115px;
  margin-bottom: 20px;
}
.title-subtext {
  font-size: 16px;
  font-family: korFont3;
  margin-top: 12px;
}
.start-btn {
  font-family: korFont1;
  font-size: 30px;
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
  text-align: center;
  bottom: 10%;
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  cursor: pointer;
  outline: inherit;
}
.main-enter-from {
  opacity: 0;
  transform: translateY(500px);
}
.main-enter-active {
  transition: all 1s ease-out;
}
.main-leave-to {
  opacity: 0;
  transform: translateY(-500px);
}
.main-leave-active {
  transition: all 1s ease-in;
}
</style>
