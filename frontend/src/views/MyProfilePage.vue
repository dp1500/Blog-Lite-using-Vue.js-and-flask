<template>
    
    
    <div>
      
      <div class="navbar">
        <NavBar />
      </div>


    <section class="h-100 gradient-custom-2">
    <div class="container w-auto py-4 h-100">
      <div class="row d-lg-flex justify-content-center align-items-center h-100 ">
        <div class="col col-lg-9 col-xl-12">
          <div class="card">
            <div class="rounded-top text-white d-flex flex-row" style="background-color: #000; height:200px;">
              <div class="ms-4 mt-5 d-flex flex-column" style="width: 150px;">
                
                <img v-if=" user_data.profile_pic_url" v-bind:src="user_data.profile_pic_url" width = "200px" height = "300"
                  alt="Generic placeholder image" class="img-fluid img-thumbnail mt-4 mb-2"
                  style="width: 150px ; z-index: 1">
                  
                <img v-else src="https://bootdey.com/img/Content/avatar/avatar7.png"
                  alt="Generic placeholder image" class="img-fluid img-thumbnail mt-4 mb-2"
                  style="width: 150px; z-index: 1">
                  
                  <!-- <a href="/" class="btn btn-secondary btn-sm" role="button" aria-pressed="true" style="z-index: 1; margin-top :50px;" >Edit Profile</a> -->
                  <a href="/EditProfile" class="btn btn-secondary btn-sm" role="button" aria-pressed="true" style="z-index: 1; margin-top: 5px;">Edit Profile</a>
                  <a href="/ProfileStatsPage" class="btn btn-secondary btn-sm" role="button" aria-pressed="true" style="z-index: 1; margin-top: 10px;">profile stats</a>
                  
                </div>

            

              <div class="ms-3" style="margin-top: 130px;">
                <h5>{{user_data.name}}</h5>
                <p>{{user_data.username}}</p>
              </div>
            </div>
            <div class="p-4 text-black" style="background-color: #f8f9fa;">
              <div class="d-flex justify-content-end text-center py-1">
                <div>
                  <p v-if="user_data.posts" class="mb-1 h5"> {{user_data.posts}} </p>
                  
                  <p v-else class="mb-1 h5"> 0 </p>
                  
                  <p class="small text-muted mb-0">Posts</p>
                </div>
                <div class="px-3">
             
                  <p v-if="user_data.n_followers" class="mb-1 h5"> {{user_data.n_followers}} </p>
                  
                  <p v-else class="mb-1 h5"> 0 </p>
                  
                  <p class="small text-muted mb-0"><a  href="/FollowersPage" class="text-muted" style="margin-left: 10px;">Followers</a></p>
                </div>
                <div>
                  
                  <p v-if="user_data.n_following" class="mb-1 h5"> {{user_data.n_following}} </p>
                  
                  <p v-else class="mb-1 h5"> 0 </p>
                  
                  <p class="small text-muted mb-0"><a  href="/FollowingPage" class="text-muted" style="margin-left: 10px;">Following</a></p>
                </div>
              </div>
            </div>
            
            <div class="card-body p-4 text-black">
              
              <div v-if="user_data.about" class="mb-2 mt-4">
                <p class="lead fw-normal mb-1">About</p>
                <div class="p-4" style="background-color: #f8f9fa;">
                  <pre id="bio-display">{{user_data.about}}</pre>
                  <!-- <p class="font-italic mb-1">{{data.about}}</p> -->
                </div>
              </div>

              <div v-if="user_data.posts" class="d-flex justify-content-between align-items-center mt-2">
                <p class="lead fw-normal mb-0">Recent posts</p>
              </div>


              <div v-else class="d-flex justify-content-between align-items-center mt-2">
                <p class="lead fw-normal mb-0">No Posts Yet</p>
              </div>

              <div v-if="isLoading" class="loading-icon">Loading...</div>

              <div  v-else class="row g-2" v-for="blog in user_blogs_data" :key="blog.blog_id">                
                
                <br>
                <hr>
                  <div class="col-sm-3 col-md-6 col-lg-4 col-xl-2">
                    <img v-bind:src="blog.image_url" class="align-self-center mr-3" width = "200px" height = "250" >
                    <br>
                    <span class="mr-2">{{ blog.likes }} Likes</span>
                    <p class="mr-2">{{ blog.n_comments }} comments</p>
                    <!-- <p class="mb-0"><a href="/" class="text-muted">View</a></p> -->
                    <!-- <p class="mb-0"><a  :href="`/EditBlogPage?blog_id=${blog.blog_id}`" class="text-muted">Edit</a></p> -->
                    <p><router-link :to="{ name: 'EditBlogPage', params: { blog_id: blog.blog_id } }">Edit Blog</router-link></p>
                    
                    
                  
                  </div>

                  <div class="col-sm-9 col-md-6 col-lg-8 col-xl-10"><h5 class="mt-0">{{ blog.title }}</h5>
                  
                  <div style="height:300px;width:1060px;border:0px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">> {{ blog.description }} </div>
                </div>

              </div>

              
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  
</div>

</template>

<style>
  .btn-custom {
    padding: 3px 8px;
    font-size: 12px;
  }
</style>

<script>

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'MyProfilePage',
  components: {
    NavBar // register the Navbar component as a local component
  },
  data() {
    return {
      errorMessage: "",
      isLoading: true,
      user_data: {},
      user_blogs_data: []
    };
  },

  methods: {

    getProfileData() {

    const token = localStorage.getItem('access_token');
    fetch('http://127.0.0.1:5000/api/ProfileData', {
      
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
    this.user_data = data;
  })
  .catch(error => {
    this.errorMessage = `An error occurred while fetching user data: ${error.message}`;
    console.error(this.errorMessage);
  });
    // finally {
    //   this.loading = false;
    // }
    },

  getProfileBlogsData() {

        const token = localStorage.getItem('access_token');
        fetch('http://127.0.0.1:5000/api/ProfileBlogsData' , {
          
        headers: {
          Authorization: `Bearer ${token}`,
        },
        })
        .then(response => {
        if (response.ok) {
          console.log("blogs data responsse was ok");
          return response.json();
        } else {
          
          return response.text().then(errorText => {
            throw new Error(`Failed to fetch Blog data: ${response.status} - ${errorText}`);
          });
        }
        })
        .then(data => {
        this.user_blogs_data = data;
        console.log(this.user_blogs_data)
        this.isLoading = false;
        })
        .catch(error => {
        this.errorMessage = `An error occurred while fetching user's Blogs data: ${error.message}`;
        console.error(this.errorMessage);
        });
        // finally {
        //   this.loading = false;
        // }
        },
  },

  created(){
      this.getProfileData()
    },
  
    mounted(){
      this.getProfileBlogsData()
    }
}
 </script>