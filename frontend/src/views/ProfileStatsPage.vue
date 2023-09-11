<template>
    <div>

      
        <NavBar />
      

      <div>

         <h2>Profile Statistics</h2>
      </div>
        <!-- <div v-if="isLoading" class="loading-icon">Loading...</div> -->
      <div v-if="isLoading" class="loading-icon">Loading...>
      </div>
      <!-- <div  v-else >  -->
      <div v-else-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>
      <div v-else>
      <ul>
        <li>total_posts: {{ stat_data.total_posts }}</li>
        <li>total_followers: {{ stat_data.total_followers }}</li>
        <li>total_following: {{ stat_data.total_following }}</li>
        <li>followers_following_ratio: {{ stat_data.followers_following_ratio}}</li>

        <li>most_liked_post_title: {{ stat_data.most_liked_post_title }}</li>
        <li>most_liked_post_likes: {{ stat_data.most_liked_post_likes }}</li>

        <li>most_commented_post_title: {{ stat_data.most_commented_post_title }}</li>
        <li>most_commented_post_n_comments: {{ stat_data.most_commented_post_n_comments }}</li>

        <li>total_likes_from_all_posts: {{ stat_data.total_likes_from_all_posts }}</li>
        <li>total_comments_from_all_posts: {{ stat_data.total_comments_from_all_posts }}</li>
        <li>total_views_from_all_posts: {{ stat_data.total_views_from_all_posts }}</li>

        <li>avg_likes_per_post: {{ stat_data.avg_likes_per_post }}</li>
        <li>avg_comments_per_post: {{ stat_data.avg_comments_per_post }}</li>
        <li>avg_engagement_rate: {{ stat_data.avg_engagement_rate }}</li>
        
      </ul>
        
      </div>

      <div>
      <h2>Data Viz</h2>
      <img :src="stat_data.graph_image_file_path" alt="Bar chart">
    </div>
     <div>
      <button @click="generatePDF">Get PDF</button>
     </div>
    </div>
  </template>


<script>

import axios from 'axios';

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'ProfileStatsPage',
  components: {
    NavBar // register the Navbar component as a local component
  },

  data() {
    return {
      errorMessage: "",
      isLoading: true,
      stat_data: {}

    };
  },

  methods: {
    getProfileStatsData() {
            const token = localStorage.getItem('access_token');
          fetch('http://127.0.0.1:5000/api/profilestats', {
            
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(response => {
          if (response.ok) {
            console.log("responsse was ok");
            this.isLoading = false;
            return response.json();
          } else {
            
            return response.text().then(errorText => {
              throw new Error(`Failed to fetch user data: ${response.status} - ${errorText}`);
            });
          }
        })
        .then(data => {
          this.stat_data = data;
        })
        .catch(error => {
          this.errorMessage = `An error occurred while fetching user data: ${error.message}`;
          console.error(this.errorMessage);
        });
          // finally {
          //   this.loading = false;
    // }
  },

      generatePDF() {
        axios.post('http://127.0.0.1:5000/generate_pdf', {
          html: this.$el.outerHTML,
          data: this.stat_data
        }).then(response => {
          console.log(response.data)
          console.log(" response for mail sent controller ok")
        }).catch(error => {
          console.log(error.response.data)
        })
      }

  },

  // created(){
  //     this.getProfileStatsData()
  //   },
  
    mounted(){
      this.getProfileStatsData()
    }

}
 </script>

<!--   

<script>

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'ProfileStatsPage',
  components: {
    NavBar // register the Navbar component as a local component
  },

    data() {
      return {
        topCommentedPost: '',
        topLikedPost: '',
        visitsThisMonth: 0,
        totalNumPosts: 0,
        avgEngagementRate: 0,
        followersFollowingRatio: 0,
        mostActiveFollower: '',
        mostFrequentHashtags: '',
        totalNumViews: 0,
        topLocation: '',
        avgTimeOnSite: 0,
      };
    },
    mounted() {
      // Fetch profile stats data from Flask RESTful API and update data properties
      fetch('http://localhost:5000/profilestats')
        .then(response => response.json())
        .then(data => {
          this.topCommentedPost = data.top_commented_post;
          this.topLikedPost = data.top_liked_post;
          this.visitsThisMonth = data.visits_this_month;
          this.totalNumPosts = data.total_num_posts;
          this.avgEngagementRate = data.avg_engagement_rate;
          this.followersFollowingRatio = data.followers_following_ratio;
          this.mostActiveFollower = data.most_active_follower;
          this.mostFrequentHashtags = data.most_frequent_hashtags;
          this.totalNumViews = data.total_num_views;
          this.topLocation = data.top_location;
          this.avgTimeOnSite = data.avg_time_on_site;
        })
        .catch(error => console.log(error));
    },
  };
  </script>
   -->