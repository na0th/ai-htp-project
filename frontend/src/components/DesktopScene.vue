<template>
  <div class="desktop-scene">
    <div class="desktop-text">
      <p class="title-text"><span style="color: #eba090">마음</span>스케치</p>
      <img class="icon1" src="../assets/images/icon5.png" />
      <p class="title-subtext">
        내가 그린 그림으로 <br />
        확인해보는 나의 심리
      </p>
      <div class="qrcode-div">
        <img class="qrcode" src="../assets/images/QR.svg.png" />
        <p class="qrcode-text">
          시작하기 위해 QR코드를 <br />핸드폰으로 스캔해주세요
        </p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "DesktopScene",
  components: {},
  data() {
    return {
      sampleData: "",
    };
  },
};
</script>
<style scoped>
.desktop-scene {
  height: calc(var(--vh, 1vh) * 100);
  background-image: url("../assets/images/desktop4.png");
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  color: black;
}
.desktop-text {
  position: absolute;
  top: 20%;
  left: 0;
  right: 0;
}
.title-text {
  font-family: korFont1;
  font-size: 55px;
}
.title-subtext {
  font-family: korFont3;
  font-size: 25px;
  margin-top: 20px;
}
.icon1 {
  margin-top: 30px;

  width: 100px;
}
.qrcode-div {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  gap: 10px;
}
.qrcode {
  width: 100px;
}
.qrcode-text {
  font-size: 13px;
  font-family: korFont2;
  line-height: 1.2;
}
</style>
