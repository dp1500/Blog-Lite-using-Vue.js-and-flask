<template>
<div class="EditBlog">

  <NavBar/> <!-- use the Navbar component here -->

  <div class="container bootstrap snippets bootdey" >
  <h2 class="text-dark" style="z-index: 1; margin-top: 15px;" >Edit Blog</h2>
  <hr>
  <form class="form-horizontal" role="form" enctype="multipart/form-data" @submit.prevent="sendNewBlogData">
    <div class="row">
      <!-- left column -->
      <div class="col-md-3">
        <div class="text-center">
          
          <img v-if="blog_data.image_url" v-bind:src="blog_data.image_url" class="avatar img-circle img-thumbnail" alt="avatar">
            
          <img v-else src="" class="avatar img-circle img-thumbnail" alt="avatar">

          <h6 class="text-dark">Upload a different photo...</h6>
          <div class="form-group mt-3">
            <label class="mr-2"></label>
            <input type="file" name="file" @change="onFileSelected">
          </div>
        </div>
      </div>

      <!-- edit form column -->
      <div class="col-lg-9 personal-info">
        <!-- <div class="alert alert-info alert-dismissable">
          <a class="panel-close close" data-dismiss="alert">×</a> 
          <i class="fa fa-coffee"></i>
          This is an <strong>.alert</strong>. Use this to show important messages to the user.
        </div> -->
        <h3 class="text-dark">Add New info</h3>

        <div class="form-group">
          <label class="col-lg-3 control-label mt-3">Title:</label>
          <div class="col-lg-8">
            <input class="form-control" id="title" name="title" type="text"  v-bind:value="blog_data.title" v-on:input="updateTitle"> 
          </div>
        </div>

        <div class="form-group">
          <label class="col-lg-3 control-label" style="z-index: 1; margin-top: 25px;">Blog description :</label>
          <div class="col-lg-8">
            <textarea class="form-control" id="description" name="description" rows="10" cols="90"  v-bind:value="blog_data.description" v-on:input="updateDescription"></textarea>
          </div>
        </div>

              <div v-if="errorMessage"
                    class= "alert alert-warning alert-dismissible fade show mt-4"
                    role="alert">
                      <strong> {{ errorMessage }} </strong>
                  </div>

                  <div v-if="response_message"
                    class= "alert alert-info alert-dismissible fade show mt-4"
                    role="alert">
                      <strong> {{ response_message }} </strong>
                  </div>  

        <button   class="btn btn-outline-primary" style="z-index: 1; margin-top: 15px;">Submit</button>
        
        <button  @click="confirmDelete()" class="btn btn-outline-danger btn-sm" style="margin-left: 119mm; margin-top: 15px;">DELETE BLOG</button>

        <br>
        <br>
      </div>
    </div>

  </form>

            
        

</div>

             

</div>

</template>


<style>
    body{margin-top:20px;}
    .avatar{
    width:200px;
    height:200px;
}			
</style>


<script>

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'EditBlogPage',
  components: {
    NavBar // register the Navbar component as a local component
  },

  data() {
    return {
      errorMessage: "",
      response_message: "",
      blog_id: this.$route.params.blog_id,
      blog_data: {},

      // ogTitle: blog_data.title,
      // ogDescription: blog_data.description,

      title: null,
      description: null,
      imageFile:null
    };
  },

  methods: {

    updateDescription(event) {
      this.description = event.target.value;
    },

    updateTitle(event) {
      this.title = event.target.value;
    },
    
    onFileSelected(event) {
            console.log(event)
            this.imageFile = event.target.files[0];
            },


    getBlogData() {

    const token = localStorage.getItem('access_token');
    fetch('http://127.0.0.1:5000/api/BlogData/'+ this.blog_id, {
      
    headers: {
      Authorization: `Bearer ${token}`,
    },
    })
    .then(response => { 
    if (response.ok) {
      console.log("blog data responsse was ok");
      return response.json();
    } else {
      
      return response.text().then(errorText => {
        throw new Error(`Failed to fetch Blog data: ${response.status} - ${errorText}`);
      });
    }
    })
    .then(data => {
    this.blog_data = data;
    console.log(this.blog_data)
    
    })
    .catch(error => {
    this.errorMessage = `An error occurred while fetching user's Blogs data: ${error.message}`;
    console.error(this.errorMessage);
    });
    // finally {
    //   this.loading = false;
    // }
},

    sendNewBlogData(){
            
            const formData = new FormData();

            if(this.imageFile != null){
              formData.append('file', this.imageFile);
              }
            
            formData.append('title', this.title);
            formData.append('description', this.description);
            
            const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000/api/BlogData/' + this.blog_id, {
              method: 'PUT',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => {

                if (response.status === 409){
                  throw new Error("file could not be uploaded");
                }

                else if (response.ok) {
                  this.response_message = "Blog Edited Succesfully"
                  this.errorMessage =""
                  setTimeout(() => {
                    this.$router.push({
                      name: 'MyProfilePage'
                      });
                    }, 3000);
                  return response.json()
                  }
                })
                // maybe create a time out function here 
            //   .then(() => {
            //     this.$router.push({
            //       name:'MyProfilePage'
            //     })
            //   })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })
            
        },

        confirmDelete() {
      if (confirm("Are you sure you want to delete this blog?")) {
    const token = localStorage.getItem('access_token');
    fetch(`http://127.0.0.1:5000/api/BlogData/${this.blog_id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(response => {
        if (response.ok) {
          this.response_message = "Blog successfully deleted";
          this.errorMessage = "";
          setTimeout(() => {
            this.$router.push({
              name: 'MyProfilePage'
            });
          }, 3000);
        } else {
          throw new Error("Failed to delete blog");
        }
      })
      .catch(error => {
        console.error('Error:', error)
        // this.errorMessage = error.message;
      });
  }
},

  },

  // beforCreated(){
  //     this.getBlogData()
  //   },


  created(){
      this.getBlogData()
    },
  
    mounted(){
      // this.sendNewBlogData()
    }

}
</script>