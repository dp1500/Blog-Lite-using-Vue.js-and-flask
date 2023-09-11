<template>
    <div class = "EditProfile">
        <NavBar></NavBar>
        
        <div class="container bootstrap snippets bootdey">
    <h3 class="text-dark">Edit Profile</h3>
    <hr>
    <form class="form-horizontal" role="form" enctype="multipart/form-data" @submit.prevent="sendNewProfileData">
        <div class="row">
            <!-- left column -->
            <div class="col-md-3">
                <div class="text-center">
                    
                    <img v-if="user_data.profile_pic__url" src="user_data.profile_pic__url" class="avatar img-circle img-thumbnail" alt="avatar">
                    
                    <img v-else src="https://bootdey.com/img/Content/avatar/avatar7.png" class="avatar img-circle img-thumbnail" alt="avatar">
                    
                    <h6 class="text-dark">Upload a different photo...</h6>
                    <div class="form-group mt-1">
                        <label class="mr-2"></label>
                        <input type="file" name="file" @change="onFileSelected">
                    </div>
                </div>
            </div>

            <!-- edit form column -->
            <div class="col-md-9 personal-info">
                <!-- <div class="alert alert-info alert-dismissable">
                <a class="panel-close close" data-dismiss="alert">×</a> 
                <i class="fa fa-coffee"></i>
                This is an <strong>.alert</strong>. Use this to show important messages to the user.
            </div> -->

                <!-- <form class="form-horizontal" role="form" method="POST"> -->
                <div class="form-group">
                    <label class="col-lg-3 control-label">Name:</label>
                    <div class="col-lg-8">
                        <input class="form-control" id="name" name="name" type="text" v-bind:value="user_data.name" v-on:input="updateName">
                    </div>
                </div>
                <br>
                <div class="form-group">
                    <label class="col-lg-3 control-label">Username:</label>
                    <div class="col-lg-8">
                        <input class="form-control" id="username" name="username" type="text" v-bind:value="user_data.username" v-on:input="updateUsername">
                    </div>
                </div>
                <br>
                <div class="form-group">
                    <label class="col-lg-3 control-label">Email Id:</label>
                    <div class="col-lg-8">
                        <input class="form-control" id="username" name="username" type="mail" v-bind:value="user_data.email" v-on:input="updateEmail">
                    </div>
                </div>
                <br>
                <div class="form-group">
                    <label class="col-lg-3 control-label">Write something about yourself:</label>
                    <div class="col-lg-8">
                        <textarea class="form-control" id="about" name="about" rows="3" cols="70" v-bind:value="user_data.about" v-on:input="updateAbout"></textarea>
                    </div>
                </div>

                <br>
                <div class="form-group">
                    <label class="col-lg-3 control-label">new password:</label>
                    <div class="col-lg-8">
                        <input class="form-control" id="new_password" name="new_password" type="password" placeholder="Leave blank for no change" v-on:input="updateNewPassword">
                    </div>
                </div>
                <br>
                <div class="form-group">
                    <label class="col-lg-6 control-label"><strong>Enter old password to make changes: </strong></label>
                    <div class="col-lg-8">
                        <input class="form-control" id="old_password" name="old_password" type="password" placeholder="old password" v-on:input="updateOldPassword">
                    </div>
                </div>
                <br>
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
                <button type="submit" class="btn btn-outline-dark">Submit</button>
                
                <button  @click="confirmDelete()" class="btn btn-outline-danger btn-sm" style="margin-left: 119mm; margin-top: 15px;">DELETE PROFILE</button>

                <!-- </form> -->
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
  name: 'EditProfile',
  components: {
    NavBar // register the Navbar component as a local component
  },

  data(){
   return {
    errorMessage: "",
    response_message: "",

    name: null,
    about: null,
    username: null,
    email: null,
    new_password: null,
    old_password: null,
    imageFile: null,
    
    user_data: {},

  };
},

methods: {

    updateName(event) {
      this.name = event.target.value;
    },
    updateEmail(event) {
      this.email = event.target.value;
    },
    updateUsername(event) {
      this.username = event.target.value;
    },
    updateAbout(event) {
      this.about = event.target.value;
    },
    updateNewPassword(event) {
      this.new_password = event.target.value;
    },
    updateOldPassword(event) {
      this.old_password = event.target.value;
    },
    
    onFileSelected(event) {
            console.log(event)
            this.imageFile = event.target.files[0];
            },

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

    sendNewProfileData(){
            
            const formData = new FormData();

            // if(!this.name || !this.username || !this.email){
            //   this.errorMessage = " 'Name', 'Username', 'Email ID' cannot be empty"
            // }

            if(!this.old_password){
              this.errorMessage = " You need to enter existing password to make changes"
            }

            else{

                if(this.imageFile != null){
              formData.append('file', this.imageFile);
              }
            

            formData.append('name', this.name);
            formData.append('username', this.name);
            formData.append('about', this.about);
            formData.append('email', this.email);
            formData.append('new_password', this.new_password);
            formData.append('old_password', this.old_password);
            
            const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000/api/ProfileData', {
              method: 'PUT',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => {

                if (response.status === 409){
                  throw new Error("Invalid Credentials");
                }
                if (response.status === 404){
                  throw new Error("Error getting user/user does not exist/auth problem");
                }

                else if (response.ok) {
                  this.response_message = "Profile Edited Succesfully"
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

            }
            
            
        },

        confirmDelete() {
              if (confirm("Are you sure you want to delete this Profile?")) {
            const token = localStorage.getItem('access_token');
            fetch(`http://127.0.0.1:5000/api/ProfileData`, {
              method: 'DELETE',
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
              .then(response => {
                if (response.ok) {
                  this.response_message = "Profile successfully deleted";
                  this.errorMessage = "";
                  setTimeout(() => {
                    this.$router.push({
                      name: 'Login_Home'
                    });
                  }, 3000);
                } else {
                  throw new Error("Failed to delete profile");
                }
              })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message;
              });
          }
      },
    },

    created(){
      this.getProfileData()
    },

}


</script>