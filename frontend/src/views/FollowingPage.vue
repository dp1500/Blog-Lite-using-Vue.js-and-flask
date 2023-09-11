<template>

    <div>

        <div class="navbar">
        <NavBar />
        </div>
        

       
<div class="row d-lg-flex justify-content-center align-items-center h-30 ">
    <div class="col col-lg-9 col-xl-12">

        <div v-for="follow in followings" :key="follow.following">

        <div class="card-body p-4 text-black" style="margin: 0cm;">

           
           
            <br>
           
                
            
            
            <div class="bg-white border mt-2" >
                <div>
                    <div class="d-flex flex-row justify-content-between align-items-center p-2 border-bottom">
                        <div class="d-flex flex-row align-items-center feed-text px-2">
                            
                            <img class="rounded-circle" v-if="follow.profile_pic_url" v-bind:src="follow.profile_pic_url" width="45">
                            
                            <img  v-else src="https://bootdey.com/img/Content/avatar/avatar7.png" class="rounded-circle" width="45">
                            

                            <div class="d-flex flex-column flex-wrap ml-2"><span class="font-weight-bold" > <router-link :to="{ name: 'UserProfilePage', params: { username: follow.username } }">
                          <span class="font-weight-bold">{{ follow.username }}</span>
                        </router-link></span></div>

                        </div> 
                        <div class="feed-icon px-2"><i class="fa fa-ellipsis-v text-black-50"></i></div>
                    </div>
                </div>
             </div>
            
            </div>
        </div>
      </div>
    </div>
  </div>

</template>


<script>
// import axios from 'axios';

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'FollowingPage',
  components: {
    NavBar // register the Navbar component as a local component
  },

  data() {
    return {
      errorMessage: "",
      response_message: "",
      isLoading: true,


      // username here refers to the username of the user whose profile is being viewed
      // username: this.$route.params.username,

      followings: []


    };
  },


 
  methods: {

    // gets the data of the blogs to be displayed on the feed page along with current user name
    getFollowingsData() {

        const token = localStorage.getItem('access_token');
        fetch('http://127.0.0.1:5000/api/followingsList', {
          
        headers: {
          Authorization: `Bearer ${token}`,
        },
        })
        .then(response => {
        if (response.ok) {

          console.log("responsse was ok");
          return response.json();
          
        } else {
          
          return response.text().then(errorText => {
            throw new Error(`Failed to fetch user data: ${response.status} - ${errorText}`);
          });
        }
        })
        .then(data => {
            console.log(data);
            this.followings = data;
            console.log("this is followings data: " + this.followings);
        })
        .catch(error => {
            this.errorMessage = `An error occurred while fetching user data: ${error.message}`;
            console.error(this.errorMessage);
        });
            // finally {
            //   this.loading = false;
            // }
        
    },

  },

  
  created() {
    this.getFollowingsData();
  }

}
  </script>
  