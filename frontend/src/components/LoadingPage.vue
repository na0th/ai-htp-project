<template>
  <ResultData v-if="data" v-bind:data="data"></ResultData>
  <div v-else class="loading-page">
    <div class="loading-text">
      <p>'마음 스케치' 프로젝트는 20대 청년들의 심리적인 문제를 해결하기...</p>
      <p class="member-text">
        프로젝트 참여 인원: <br /><br />
        Front-End: 이윤영, 최건 <br />
        Back-End: 양채린, 황혜수, 백소미 <br />
        AI: 이수민, 이겸희 <br />Design: 이가윤
      </p>
    </div>
    <p class="touch-text1">잠시만 기다려주세요...</p>
  </div>
</template>

<script>
import ResultData from "../views/Result/ResultData.vue";
export default {
  name: "LoadingPage",
  components: { ResultData },
  props: ["data"],
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.loading-page {
  height: calc(var(--vh, 1vh) * 100);
  background: #4d4d4d;
  font-family: korFont2;
}
.loading-text {
  line-height: 1.3;
  width: 85%;
  font-family: korFont2;
  display: flex;
  flex-direction: column;
  text-align: left;
  padding-left: 25px;
  padding-top: 50px;
  font-size: 25px;
}
.loading-text:first-child {
  font-size: 20px;
}
.member-text {
  padding-top: 150px;
  font-size: 20px;
}
.touch-text1 {
  color: #dededeb9;
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
  text-align: center;
  bottom: 20%;
  font-size: 17px;
  animation: blinker 2s linear infinite;
}
</style>
