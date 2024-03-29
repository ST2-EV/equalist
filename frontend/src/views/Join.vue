<template>
  <div class="header">
    <img src="../assets/Logo.svg" alt="logo" id="logo" />
  </div>
  <Loading />
</template>

<script>
import { options } from "../assets/backend-url";
import Loading from "../components/Loading.vue";
export default {
  components: { Loading },
  beforeCreate() {
    const opts = {
      join_code: this.$route.params.id,
    };
    fetch(options.url + "confirm", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(opts),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data["name"] !== undefined) {
          this.$swal({
            title: "Would you like to join " + data["name"] + "?",
            text: data["number_online"] + " have joined so far!", // you are the first one to join | 1 has joined so far
            showDenyButton: true,
            denyButtonText: `Cancel`,
            confirmButtonText: `Yes`,
            confirmButtonColor: "#505690",
            icon: "question",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location = options.url + "oauth/" + this.$route.params.id;
            } else if (result.isDenied) {
              this.$router.push("/"); // user denied to join room
            }
          });
        } else{
           this.$swal({
          title: "The join code you entered doesnt seem to exist.",
          icon: "info",
        }).then(()=>this.$router.push("/"))
        }
      })
      .catch((error) => {
        this.$swal({
          title: "Something went wrong please try again",
          icon: "info",
        }).then(()=>this.$router.go())
      });
  },
};
</script>