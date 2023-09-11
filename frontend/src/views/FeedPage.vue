<template>

  

  <div>
    
    <div class="navbar">
    <NavBar />
    </div>

    <h3 class="mt-4">Hi {{ logged_user_name }}</h3>
    <h3 v-if="logged_user_followings < 1"> Follow people to see posts</h3>

    <h3 v-else>
      <template v-if="!blogData">
        WELCOME TO YOUR FEED. Follow more People to see what they are posting
      </template>
      <template v-else>
        WELCOME TO YOUR FEED. SEE WHAT'S COOKING!
      </template>
    </h3>
    <br>

    <div class="row d-lg-flex justify-content-center align-items-center h-100">
      <div class="col col-lg-9 col-xl-12">
        <div class="card-body p-4 text-black">
          <div class="row g-2">

            <div v-if="isLoading" class="loading-icon">Loading...</div>

            <div v-else class="row g-2" v-for="blog_data in blog_data" :key="blog_data.blog_id">


              <div class="card bg-white border mt-4">
                <div class="card-header">
                  <div class="d-flex flex-row justify-content-between align-items-center p-2 border-bottom">
                    <div class="d-flex flex-row align-items-center feed-text px-2">
                      <img class="rounded-circle" v-bind:src="blog_data.profile_pic_url" width="45">
                      <div class="d-flex flex-column flex-wrap ml-2">
                        <router-link :to="{ name: 'UserProfilePage', params: { username: blog_data.username } }">
                          <span class="font-weight-bold">{{ blog_data.username }}</span>
                        </router-link>
                      </div>
                    </div>
                    <div class="feed-icon px-2">
                      <i class="fa fa-ellipsis-v text-black-50"></i>
                    </div>
                  </div>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-sm-3 col-md-6 col-lg-4 col-xl-2">
                      <img v-bind:src="blog_data.image_url" class="align-self-center mr-3" width="200px" height="250">
                    </div>
                    <div class="col-sm-9 col-md-6 col-lg-8 col-xl-10">
                      <h5 class="card-title">{{ blog_data.title }}</h5>
                      <!-- <textarea class="form-control" v-model="blog_data.content" rows="5" cols="50" readonly></textarea> -->
                      <div style="height:300px;width:1200px;border:0px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">> {{ blog_data.description }} </div>
                      <!-- <p class="card-text">{{ blog_data.description }}</p> -->
                    </div>

                  </div>
                </div>
                <div class="card-footer text-muted">
                  <div class="d-flex flex-row justify-content-between align-items-center p-2 border-bottom">
                    <div class="d-flex flex-row align-items-center feed-text px-2">
                      <span class="mr-2">{{ blog_data.likes }} Likes</span>
                      
                        <button  @click="() => toggleLike(blog_data.blog_id)">
                          <i class="fas fa-heart"></i> Like
                        </button>
                    </div>

                    <div class="d-flex flex-row align-items-center feed-text px-2">
                      <span class="mr-2 text-button" @click="() => openComments(blog_data.blog_id)">{{ blog_data.n_comments }} Comments</span>

                      <!-- <router-link :to="{ name: 'BlogPage', params: { username: blog_data.username, blog_id: blog_data.blog_id } }">
                        <button class="btn btn-primary">
                          Read More
                  </button>
                </router-link> -->


              </div>

              

            </div>

              
            <!-- <div v-if="showComments">
                      <div  v-for="comment in comments" :key="comment.id" >
                        <div v-if="blog_data.blog_id == comment.blog_id">
                        <div class="d-flex align-items-center mb-2" >
                          <img :src="comment.profile_pic_url" class="mr-2" style="width: 30px; height: 30px; object-fit: cover; border-radius: 50%;" alt="Profile Picture">
                          <span class="font-weight-bold">{{ comment.username }}</span>
                        </div>
                        <div>{{ comment.comment }}</div>
                      </div>
                    </div>
                    <form @submit.prevent="submitComment(blog_data.blog_id)">
                        <textarea v-model="newComment"></textarea>
                        <button type="submit">Add Comment</button>
                      </form>
                </div> -->

                <div v-if="showComments" class="comments-section" >
                  <div v-if="flag_blog_id === blog_data.blog_id">
                    
                  
                  <div v-for="comment in comments" :key="comment.id" class="comment">
                    <div v-if="blog_data.blog_id == comment.blog_id">
                      <div class="d-flex align-items-center mb-2">
                        <img :src="comment.profile_pic_url" class="mr-2 profile-pic" alt="Profile Picture">
                        <span class="font-weight-bold">{{ comment.username }}</span>
                      </div>
                      <div class="comment-text">{{ comment.comment }}</div>
                    </div>
                  </div>
                </div>
                  <form @submit.prevent="submitComment(blog_data.blog_id)" class="comment-form">
                    <textarea v-model="newComment" class="comment-box"></textarea>
                    <button type="submit" class="btn btn-primary">Add Comment</button>
                  </form>
                </div>

            

          </div>
        </div>
        <div v-if="!isLoading && blogData && blogData.length < 1" class="no-data-text">No Posts found in your feed</div>
      </div>
    </div>
  </div>
</div>

</div>

</div>
</template>

<style>

.navbar {
  margin: 0;
  padding: 0;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 999;
}

.feed {
  padding-top: 70px;
  padding-bottom: 50px;
  background-color: #f5f5f5;
  min-height: 100vh;
}


.card {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2);
}

.card-header {
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  padding: 5px 10px;
}

.card-footer {
  background-color: #fff;
  border-top: 1px solid #ddd;
  padding: 5px 10px;
}

.card-body {
  padding: 10px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.card-text {
  font-size: 1.1rem;
}

.loading-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  height: 80vh;
}

.no-data-text {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  height: 70vh;
}

.comments-section {
  margin-top: 10px;
}

.comment {
  padding: 10px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
}

.profile-pic {
  width: 30px;
  height: 30px;
  object-fit: cover;
  border-radius: 50%;
}

.comment-text {
  margin-top: 5px;
}

.comment-box {
  width: 100%;
  height: 50px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 10px;
}

.btn-primary {
  background-color: blue;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  margin-top: 10px;
}


</style>


<script>
import axios from 'axios';

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'FeedPage',
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

      logged_user_name: "",
      logged_user_followings: null,
      blog_data: [],
      // user_blogs_data: []

      // for like unlike functionality
      isLiked: false,

      // for comments
      showComments: false,
      flag_blog_id: null,
      comments: [],
      newComment: '',

    };
  },
  
  computed: {
    // get() {
    //     return this.blog_data.isLiked || false; // return the isLiked value from the blog_data prop or false if it is undefined
    //   },
    //   set(value) {
    //     this.blog_data.isLiked = value; // update the isLiked value in the blog_data prop
    //   }
  },


 
  methods: {

    // gets the data of the blogs to be displayed on the feed page along with current user name
    getFeedBlogsData() {

        const token = localStorage.getItem('access_token');
        fetch('http://127.0.0.1:5000/api/FeedBlogsData', {
          
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
        this.blog_data = data["blogsData"];
        this.logged_user_name = data["logged_user_name"],
        this.logged_user_followings = data["logged_user_followings"],

        this.isLoading = false;
        console.log(this.blog_data);
        })
        .catch(error => {
        this.errorMessage = `An error occurred while fetching blogs data: ${error.message}`;
        console.error(this.errorMessage);
        });
        // finally {
        //   this.loading = false;
        // }
        },

        toggleLike(blog_id) {
      const url = `http://127.0.0.1:5000/api/LikePost/${blog_id}`; // construct the URL for the API endpoint with the blog_id parameter
      
      axios.post(url)
        .then(response => {
          // this.blog_data.likes = response.data.likes; // update the like count in your blog post data
          this.liked = response.data.isLiked; // update the liked state in your component
        })
        .catch(error => {
          console.error(error);
        });
        this.getFeedBlogsData()
    },

    openComments(blog_id) {
      this.comments = [];
      this.showComments = true;
      console.log("show comments turned: " + this.showComments);
      this.flag_blog_id = blog_id;
      console.log("blog id is: " + blog_id);
      console.log("flag blog id is: " + this.flag_blog_id);
       // fetch comments for current blog post
      axios.get(`http://127.0.0.1:5000/api/comments/${blog_id}`)
      .then(response => {
      this.comments = response.data;
      })
      .catch(error => {
      console.error(error);
       });
    },

    updateFlag(blog_id) {
        this.flag_blog_id = blog_id;
        console.log("flag blog id is: " + this.flag_blog_id);
      },

    submitComment(blog_id) {

          const formData = new FormData();

            formData.append('comment', this.newComment);
            
            const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000/api/comments/' + blog_id, {

              // fetch('http://127.0.0.1:5000//api/comments/${blog_id}', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => response.json())
              .then(data => {
                // this.comments.push(response.data);
                // this.newComment = '';      
                this.comments = [];
                this.comments.push(data); // add the new comment to the comments array
                this.newComment = ''; // reset the new comment input field
                alert('Comment added successfully!'); // show an alert message
                this.getFeedBlogsData()
                })
              .catch(error => {
                console.error('Error:', error)
                
              })
            
        },

  },

  
    

  mounted(){
    this.getFeedBlogsData()
  }


}
  </script>
  