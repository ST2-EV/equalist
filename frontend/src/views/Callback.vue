<template>
  <div class="header">
    <img src="@/assets/Logo.svg" alt="logo" id="logo" />
  </div>
  <Loading :text="false" />
</template>

<script>
import { options } from '@/assets/backend-url';
import Loading from "@/components/Loading.vue"
export default {
  components:{
    Loading,
  },
  title: "loading...",
  data() {
      return{
          message: ""
      }
  },
  mounted() {
    const code = this.$route.query.code;
    const state = this.$route.query.state;
    if ((code !== undefined) && (state === 'none')) {
      const data = { code: code, state: state };
      fetch(options.url + "login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          if ((data["user_id"] !== undefined) && (data["user_id"] !== undefined)) {
            localStorage.setItem('user_id', data["user_id"])
            localStorage.setItem('room_id', data["room_id"])
            this.$router.push('waiting-room')
          } else {
            this.$router.push("/")
          }
        })
        .catch((error) => {
          this.$router.push("/")
        });
    } else if((code !== undefined) && (state !== 'none')){
      const data = { code: code, room_id: state };
      console.log(data)
      fetch(options.url + "join", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          this.$router.push('success')
        })
        .catch((error) => {
          this.$router.push("/")
        });
    }
    else{
        this.$router.push("/")
    }
  },
};
</script>