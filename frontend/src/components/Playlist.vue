<template>
  <div class="container">
    <section id="playlist">
      <div id="cover">
        <span>{{ date }}</span>
        <!-- <img :src="playlistImage" alt="cover-image" /> -->
        <div ref="putImageHere" style="display:flex; justify-content:center;"></div>
      </div>
      <div id="playlist-info">
        <div>
          <h1>
            {{ truncate(name, 7)}}'s <br />
            <span>playlist</span>
          </h1>
        </div>
        <div id="controls">
          <div id="res-div" @click.prevent="restartPop">
            <img src="../assets/restart.png" />
          </div>
          <div id="play-div" @click.prevent="redirect">
            <img src="../assets/play.png" id="play" />
          </div>
        </div>
      </div>
    </section>
     
  </div>
</template>

<script>
import { options } from '../assets/backend-url';
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'
export default {
  props: {
    playlistURL: String,
    playlistImage: Object,
    name: String,
    date: String,
    restart: { type: Function },
    loading: { type: Function },
  },
  methods: {
    redirect() {
      this.addToAnalytics("play")
      window.open(this.playlistURL, '_blank');
    },
    restartPop() {
      this.$swal({
        title: "Are you sure you want to restart the process?",
        showCancelButton: true,
        cancelButtonColor: `grey`,
        confirmButtonText: `Yes`,
        confirmButtonColor: "#505690",
        icon: "question",
      }).then((result) => {
        if (result.isConfirmed) {
          this.addToAnalytics("restart")
          this.loading()
          let opts = {
            user_id: localStorage.getItem("user_id")
          };
          fetch(options.url + "create-room", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(opts),
          })
          .then((response) => response.json())
          .then((data) => {
            localStorage.setItem('user_id', data["user_id"])
            localStorage.setItem('room_id', data["room_id"])
            this.restart()        
          })
          .catch((error) => {
            localStorage.clear()
            this.$router.push("/")
          })
        }});
    },
    truncate: function (data, num) {
      const reqdString = data.split("").slice(0, num).join("");
      return reqdString;
    }
  },
  mounted() {
    console.log(this.playlistImage)
    this.playlistImage.style.width="75%"
    this.playlistImage.style.zIndex = "300"
    this.playlistImage.style.boxShadow = "0 3px 5.2px rgba(0, 0, 0, 0.02), 0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),0 109px 188px rgba(0, 0, 0, 0.07)";
    this.$refs.putImageHere.appendChild(this.playlistImage)
    createToast("Consider adding equalist to your home screen.", {timeout: 3000, position:'bottom-center'})

  }
};
</script>

<style scoped>

/* playlist portion */
.container {
  display: flex;
  height: calc(100vh - 205px);
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}

#playlist {
  margin-left: 40px;
  margin-right: 40px;
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  align-items: center;
  background-color: white;
  padding: 40px 40px 50px 40px;
  border-radius: 29px;
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}
#cover {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
@keyframes slideInFromBottom {
  0% {
    transform: translateY(40%);
  }
  100% {
    transform: translateX(0);
  }
}
#cover span {
  animation: 1s ease-out 0s 1 slideInFromBottom;
  background: -webkit-linear-gradient(
    -90deg,
    #653277 0%,
    #505690 15.62%,
    #5f679c 33.33%,
    #6e79a9 48.44%,
    #8b9bc1 65.62%,
    #c7e1f3 85.42%
  );
  background: -webkit-linear-gradient(
    -90deg,
    #653277 0%,
    #505690 15.62%,
    #5f679c 33.33%,
    #6e79a9 48.44%,
    #8b9bc1 65.62%,
    #c7e1f3 85.42%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 2.5rem;
}
.covimg {
  z-index: 100;
  width: 70%;
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}

#playlist-info {
  padding-left: 40px;
  padding-right: 40px;
}

#playlist-info div h1 {
  font-size: 2rem;
  text-align: center;
}

#playlist-info div h1 span {
  color: #505690;
}

#controls {
  display: flex;
}
#controls div {
  cursor: pointer;
  background-color: #505690;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  padding: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}
#controls div:hover {
  transform: scale(1.03);
}

#controls div:active {
  transform: scale(0.98);
}
.shadow {
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}

#controls div img {
  width: 70%;
  padding-left: 1px;
  padding-bottom: 1px;
}

#res-div {
  margin-right: 10px;
  z-index: 100;
}

#play {
  padding-left: 5px !important;
  width: 62% !important;
}
/* roll in */
#play-div {
  animation: 0.8s ease-in-out 0s 1 rollIn;
}
@keyframes rollIn {
  0% {
    transform: translateX(-100%) rotate(-180deg);
    opacity: 0%;
    box-shadow: none;
  }
  100% {
    transform: translateX(0) rotate(0deg);
  }
}
/* for iphone se */
@media only screen and (max-device-width: 320px) {
  .container {
    height: calc(100vh - 180px);
  }
  #playlist {
    padding: 0px 10px 20px 10px;
  }
}
</style>