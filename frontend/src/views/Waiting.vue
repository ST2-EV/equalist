<template >
  <div class="header">
    <img src="../assets/Logo.svg" alt="logo" id="logo" />
  </div>
  <transition name="slide" mode="out-in">
    <Loading v-if="loading" key="loading" />
    <div v-else-if="playlistCreated" key="playlist">
        <Playlist
          :date="date"
          :playlistURL="playlistURL"
          :playlistImage="playlistImage"
          :name="creator"
          :restart="restartProcess"
          :loading="setLoading"
        />
    </div>
    <div v-else key="info">
      <!-- <transition appear name="fade"> -->
        <div>
          <section id="info">
            <div id="info-card" class="shadow">
              <div id="name-tag">
                {{ creator }}'s <br />
                <span>room</span>
              </div>

              <div id="link">
                <div class="tooltip">
                  <div
                    id="link-inp"
                    :class="[clicked ? '' : 'animate']"
                    @click.prevent="copyToClipBoard"
                  >
                    {{ invite }}
                  </div>
                  <a
                    id="btn2"
                    href="#"
                    title="Copy"
                    @click.prevent="copyToClipBoard"
                  >
                    <img src="../assets/copy.png" alt="copy" id="copy" />
                  </a>
                  <span :id="[copied ? 'tooltiptext' : 'hidden']">
                    Copied!
                  </span>
                </div>
                <a
                  id="asd"
                  class="btn shadow"
                  href="#"
                  title="Create Playlist"
                  @click.prevent="submit"
                >
                  Let's Gooo
                </a>
              </div>
            </div>

            <div id="friends">
              <transition-group name="list">
                <div class="user" v-for="friend in friends" :key="friend.name">
                  <Avataaar class="image" :identifier="friend.identifier" />
                  {{ friend.name }}
                </div>
              </transition-group>
              <div id="dummy" v-if="friends.length % 2 !== 0"></div>
            </div>

            <div id="friends-place" v-if="friends.length === 0">
              <div>Share the link above with your friends to add them!</div>
            </div>
          </section>
        </div>
      <!-- </transition> -->
    </div>
  </transition>
</template>
<script>
import useClipboard from "vue-clipboard3";

import Avataaar from "@/components/Avataaars.vue";
import Loading from "@/components/Loading.vue";
import Playlist from "@/components/Playlist.vue";
import { options } from "@/assets/backend-url.js";

const newFriendNotification = new Audio('file://@/assets/ten.mp3');
export default {
  title() {
    return `Your room`;
  },
  components: {
    Avataaar,
    Loading,
    Playlist,
  },
  data() {
    return {
      loading: true,
      post: false,
      copied: false,
      creator: "",
      invite: "",
      friends: [],
      playlistCreated: false,
      playlistURL: "",
      playlistImage: "",
      date: "",
      clicked: false,
      interval: "",
    };
  },
  methods: {
    async copyToClipBoard() {
      const { toClipboard } = useClipboard();
      try {
        await toClipboard(
          "Click here to join my playlist! => https://" + this.invite
        );
        this.copied = true;
        setTimeout(() => (this.copied = false), 1200);
        this.clicked = true;
        setTimeout(() => (this.clicked = false), 10000);
      } catch (e) {
        console.error(e);
      }
    },
    submit() {
      if (this.friends.length === 0) {
        this.$swal({
          title: "You need atleast one friend to make the playlist!",
          icon: "info",
        });
      } else {
        this.addToAnalytics("create-playlist")
        clearInterval(this.interval)
        this.loading = true;
        const opts = {
          user_id: localStorage.getItem("user_id"),
          room_id: localStorage.getItem("room_id"),
        };
        fetch(options.url + "create-playlist", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(opts),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data)
            this.playlistURL = data["playlist_url"];
            const cover = new Image(); 
            cover.src = data["playlist_cover"]
            this.playlistImage = cover;
            this.date = data["date"];
            this.loading = false;
            this.playlistCreated = true;
          })
          .catch((error) => {
            console.log(error)
          });
      }
    },
    restartProcess() {
      this.fetchRoom();
      this.playlistCreated = false;
      this.loading = false;
    },
    setLoading() {
      this.loading = true;
    },
    sound() {
      newFriendNotification.play();
    },
    fetchRoom() {
      this.loading = true;
      let opts = {
        user_id: localStorage.getItem("user_id"),
        room_id: localStorage.getItem("room_id"),
      };
      fetch(options.url + "room-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(opts),
      })
        .then((response) => response.json())
        .then((data) => {
          this.loading = true;
          if (!data["active"]) {
            this.playlistCreated = true;
            let len = data["name"].length - 7;
            this.creator = data["name"].substring(0, len);
            this.playlistURL = data["playlist_url"];
            const cover = new Image(); 
            cover.src = data["playlist_cover"]
            this.playlistImage = cover;
            this.date = data["date"];
            this.loading = false;
          } else {
            let len = data["name"].length - 7;
            this.creator = data["name"].substring(0, len);
            this.invite = "equalist.xyz/j/" + data["join_code"];
            data["people"].reverse();
            this.friends = data["people"];
            this.loading = false;
            setInterval(this.pollforFriends, 2000);
          }
        })
        .catch((error) => {
          localStorage.clear();
          this.$router.push("/");
        });
    },
    pollforFriends() {
      const user_id = localStorage.getItem("user_id");
      const room_id = localStorage.getItem("room_id");
      if (user_id !== null && room_id !== null) {
        fetch(options.url + "friends/" + user_id + "/" + room_id)
          .then((response) => response.json())
          .then((data) => {
            if (data["friends"].length !== this.friends.length) {
              this.sound();
            }
            data["friends"].reverse();
            this.friends = data["friends"];
          })
          .catch((error) => {
            console.log("get-friends failed");
            this.$router.go();
          });
      } else {
        localStorage.clear();
        this.$router.push("/");
      }
    },
  },
  mounted() {
    this.loading = true;
    if (localStorage.getItem("user_id") === null) {
      localStorage.clear();
      this.$router.push("/");
    }

    if (localStorage.getItem("room_id") !== null) {
      this.addToAnalytics("create")
      let opts = {
        user_id: localStorage.getItem("user_id"),
        room_id: localStorage.getItem("room_id"),
      };
      fetch(options.url + "room-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(opts),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data["active"]) {
            this.playlistCreated = true;
            let len = data["name"].length - 7;
            this.creator = data["name"].substring(0, len);
            this.playlistURL = data["playlist_url"];
            const cover = new Image(); 
            cover.src = data["playlist_cover"]
            this.playlistImage = cover;
            this.date = data["date"];
            this.loading = false;
          } else {
            let len = data["name"].length - 7;
            this.creator = data["name"].substring(0, len);
            this.invite = "equalist.xyz/j/" + data["join_code"];
            data["people"].reverse();
            this.friends = data["people"];
            this.loading = false;
            this.interval = setInterval(this.pollforFriends, 2000);
          }
        })
        .catch((error) => {
          localStorage.clear();
          this.$router.push("/");
        });
    } else {
      localStorage.clear();
      this.$router.push("/");
    }
  },
};
</script>

<style scoped>
/* transitions */

/* friends placeholder */
#friends-place {
  background-color: white;
  border-radius: 15px;
  padding: 15px 25px;
  width: 40%;
  font-size: 1.1rem;
}
#friends-place div {
  text-align: center;
}

@media only screen and (max-device-width: 500px) {
  #friends-place {
    width: 60%;
  }
}
/* friends list */
.list-enter-active,
.list-leave-active,
.list-move {
  transition: 500ms cubic-bezier(0.59, 0.12, 0.34, 0.95);
  transition-property: opacity, transform;
}

.list-enter {
  opacity: 0;
  transform: translateX(50px) scaleY(0.5);
}

.list-enter-to {
  opacity: 1;
  transform: translateX(0) scaleY(1);
}

/* waiting-room section */

.fade-enter-active,
.fade-leave-active,
.fade-move{
  transition: 0.5s ease;
  transition-property: opacity, transform;
}

.fade-enter {
  opacity: 0.2;
  transform: translateY(8%);
}

.fade-enter-to {
  transform: translateY(0%);
  opacity: 1;
}

/* .fade-enter-active {
  animation: go 0.5s ease;
}

@keyframes go {
  from {
    transform: translateY(8%);
    opacity: 20%;
  }
  to {
    transform: translateY(0%);
    opacity: 100%;
  }
} */

/* playlist section */
/* 
.pop-enter-active {
  animation: pop 0.5s ease;

}

@keyframes pop {
  from {
    transform: scale(0.5);
    opacity: 20%;
    
  }
  to {
    transform: scale(1);
    opacity: 100%;
  }
} */

/* transition to loading */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s ease-in-out;
  /* transition-property: opacity transform; */
}

.slide-enter-from {
  transform: scale(0.5);
  opacity: 0;
}

.slide-enter-to {
  transform: scale(1);
  opacity: 1;
}

.slide-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

/* Tooltip for "copy" */
.tooltip {
  position: relative;
}
@keyframes slideInFromBottom {
  0% {
    transform: translateY(50%);
    opacity: 0.5;
  }
  100% {
    transform: translateX(0);
    opacity: 0.9;
  }
}
/* Tooltip text */
#tooltiptext {
  animation: 0.2s ease-out slideInFromBottom;
  width: 30%;
  opacity: 0.9;
  background-color: #505690;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 10;
  bottom: 90%;
  left: 96%;
  margin-left: -60px;
}

#hidden {
  display: none;
}
/* Info section */
#info {
  margin-top: 37px;
  width: 100%;
  /* height: calc(100vh - 200px); */
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  align-items: center;
}

#info-card {
  display: flex;
  background-color: white;
  width: 40%;

  justify-content: space-evenly;
  align-items: center;

  border-radius: 25px;
  flex-wrap: wrap;

  padding: 20px 70px 20px 70px;
}

#name-tag {
  font-size: 250%;
  text-align: center;
  margin: 10px;
}

#name-tag span {
  color: #505690;
}

.btn {
  text-decoration: none;
  color: white;
  background-color: #505690;
  padding: 20px;
  border-radius: 13px;
  font-size: 2rem;
  text-align: center;
  margin: 0 10px 10px 10px;
}

.btn:hover {
  transform: scale(1.03);
}

.btn:active {
  transform: scale(0.98);
}

.shadow {
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}

#link {
  display: flex;
  flex-direction: column;
}

#link div {
  display: flex;
  padding: 10px;
}

#btn2 {
  text-decoration: none;
  background-color: #505690;
  border-radius: 9px;
  cursor: pointer;
  display: table-cell;
  text-align: center;
  vertical-align: middle;
}
#btn2:hover {
  transform: scale(1.03);
}

#btn2:active {
  transform: scale(0.98);
}

#link-inp {
  border-radius: 13px;
  padding: 10px;
  margin-right: 8px;
  border: 4px solid #505690;
  color: #505690;
}

.animate {
  animation: 1s bounce-5 ease infinite;
  animation-delay: 1.5s;
}

@keyframes bounce-5 {
  0% {
    transform: scale(1, 1) translateY(0);
  }
  10% {
    transform: scale(1, 1) translateY(0);
  }
  30% {
    transform: scale(1, 1) translateY(-5px);
  }
  50% {
    transform: scale(1, 1) translateY(0);
  }
  57% {
    transform: scale(1, 1) translateY(-1px);
  }
  64% {
    transform: scale(1, 1) translateY(0);
  }
  100% {
    transform: scale(1, 1) translateY(0);
  }
}

#copy {
  width: 25px;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;

  vertical-align: middle;
}

@media only screen and (min-device-width: 1059px) {
  #link {
    display: flex;
    flex-direction: column;
    padding-top: 30px;
    padding-bottom: 30px;
  }

  #info-card {
    display: flex;
    background-color: white;
    width: 40%;

    justify-content: space-evenly;
    align-items: center;

    border-radius: 25px;
    flex-wrap: wrap;

    padding: 20px 20px 20px 20px;
  }
  #friends {
    width: 42% !important;
  }
  #friends div {
    flex: 1 0 35% !important;
  }
  .user:nth-child(even) {
    margin-left: 15px;
  }
  #dummy {
    margin-top: 15px;
    margin-left: 15px;
    border-radius: 25px;
    padding: 10px;
  }
}
@media only screen and (max-device-width: 400px) {
  #info-card {
    display: flex;
    background-color: white;
    width: 40%;

    justify-content: space-evenly;
    align-items: center;

    border-radius: 25px;
    flex-wrap: wrap;

    padding: 20px 70px 20px 70px;
  }

  #friends {
    width: 79% !important;
  }
}

@media only screen and (max-device-width: 1058px) and (min-device-width: 700px) {
  #info-card {
    display: flex;
    background-color: white;
    width: 40%;

    justify-content: space-evenly;
    align-items: center;

    border-radius: 25px;
    flex-wrap: wrap;

    padding: 20px 0px 20px 0px;
  }

  #friends {
    width: 40% !important;
  }
}

@media only screen and (min-device-width: 1650px) {
  #info-card {
    display: flex;
    background-color: white;
    width: 30%;

    justify-content: space-evenly;
    align-items: center;

    border-radius: 25px;
    flex-wrap: wrap;

    padding: 20px 0px 20px 0px;
  }
  #friends {
    width: 29% !important;
  }
  #friends div {
    flex: 1 0 40% !important;
  }
}

/* Friend's section */
#friends {
  /* margin-top: 20px; */
  width: 72%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-bottom: 15px;
  margin-top: 15px;
}

.user {
  margin-top: 15px;
  background-color: white;
  flex: 1 0 46%;
  border-radius: 25px;
  padding: 10px;
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-size: 2rem;
}

.user .image {
  width: 20%;
  padding-right: 15px;
}
</style>