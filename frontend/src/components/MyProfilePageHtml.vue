<!-- <template>
    
    <section class="h-100 gradient-custom-2">
    <!-- <div class="container w-auto py-4 h-100"> -->
      <div class="row d-lg-flex justify-content-center align-items-center h-100 ">
        <div class="col col-lg-9 col-xl-12">
          <div class="card">
            <div class="rounded-top text-white d-flex flex-row" style="background-color: #000; height:200px;">
              <div class="ms-4 mt-5 d-flex flex-column" style="width: 150px;">
                {% if data.profile_pic_url %}
                <img src= "{{data.profile_pic_url}} " width = "200px" height = "300"
                  alt="Generic placeholder image" class="img-fluid img-thumbnail mt-4 mb-2"
                  style="width: 150px ; z-index: 1">
                  {% else %} 
                <img src="https://bootdey.com/img/Content/avatar/avatar7.png"
                  alt="Generic placeholder image" class="img-fluid img-thumbnail mt-4 mb-2"
                  style="width: 150px; z-index: 1">
                  {% endif %}
                  <a href="{{url_for('edit_profile')}}" class="btn btn-secondary btn-sm" role="button" aria-pressed="true" style="z-index: 1; margin-top :50px;" >Edit Profile</a>

                
                  <!-- <button type="button" class="btn btn-outline-dark" data-mdb-ripple-color="dark"
                  style="z-index: 1;">
                  Edit profile
                </button> -->
              </div>
              <div class="ms-3" style="margin-top: 130px;">
                <h5>{{data.name}}</h5>
                <p>{{data.username}}</p>
              </div>
            </div>
            <div class="p-4 text-black" style="background-color: #f8f9fa;">
              <div class="d-flex justify-content-end text-center py-1">
                <div>
                  {% if data.posts %}
                  <p class="mb-1 h5"> {{data.posts}} </p>
                  {% else %}
                  <p class="mb-1 h5"> 0 </p>
                  {% endif %}
                  <p class="small text-muted mb-0">Posts</p>
                </div>
                <div class="px-3">
                  {% if data.n_followers %}
                  <p class="mb-1 h5"> {{data.n_followers}} </p>
                  {% else %}
                  <p class="mb-1 h5"> 0 </p>
                  {% endif %}
                  <p class="small text-muted mb-0"><a  href="/followers/{{data.Uid}}" class="text-muted" style="margin-left: 10px;">Followers</a></p>
                </div>
                <div>
                  
                  {% if data.n_following %}
                  <p class="mb-1 h5"> {{data.n_following}} </p>
                  {% else %}
                  <p class="mb-1 h5"> 0 </p>
                  {% endif %}
                  <p class="small text-muted mb-0"><a  href="/following/{{data.Uid}}" class="text-muted" style="margin-left: 10px;">Following</a></p>
                </div>
              </div>
            </div>
            
            <div class="card-body p-4 text-black">
              {% if data.about %}
              <div class="mb-5">
                <p class="lead fw-normal mb-1">About</p>
                <div class="p-4" style="background-color: #f8f9fa;">
                  <pre id="bio-display">{{data.about}}</pre>
                  <!-- <p class="font-italic mb-1">{{data.about}}</p> -->
                </div>
                {% endif %}
              </div>

              <div class="d-flex justify-content-between align-items-center mb-4">
                <p class="lead fw-normal mb-0">Recent posts</p>
                
              </div>

              <div class="row g-2">

                <!-- <div class="container">
                  <div class="row">
                    {% for blog in blog_data %}
                    <div class="col-sm-4">
                      <div class="card">
                        <img src="{{ blog.image_url }}" class="card-img-top" alt="{{ blog.title }}">
                        <div class="card-body">
                          <h5 class="card-title">{{ blog.title }}</h5>
                          <p class="card-text">{{ blog.description }}</p>
                        </div>
                      </div>
                    </div>
                    {% endfor %}
                  </div>
                </div> -->

                <!-- LAYPUT 2 -->
                {% for blog in blog_data %}
                <br>
                <hr>
                  <div class="col-sm-3 col-md-6 col-lg-4 col-xl-2">
                    <img src="{{ blog.image_url }}" class="align-self-center mr-3" width = "200px", height = "250" >
                    <br>
                    <p class="mb-0"><a href="/blog/{{blog.username}}/{{blog.blog_id}}" class="text-muted">View</a></p>
                    <p class="mb-0"><a href='/EditBlog/{{blog.blog_id}}' class="text-muted">Edit</a></p>
                    
                    <!-- <script>
                      var parameterValue = '{{blog.blog_id}}';
                    </script> -->
                    
                    <!-- <button class="btn btn-outline-DANGER" onclick="confirmDelete()" style="height:30px;width:80px">Delete</button> -->

                  
                  </div>
                  
                  <!-- <div class="col-sm- col-md-1 col-lg-8 col-xl-1">
                        hello
                  </div> -->

                  <div class="col-sm-9 col-md-6 col-lg-8 col-xl-10"><h5 class="mt-0">{{ blog.title }}</h5>
                  
                  <div style="height:300px;width:1060px;border:0px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">> {{ blog.description }} </div>
                </div>
                  
                <!-- <div class="media">
                  <img src="{{ blog.image_url }}" class="align-self-center mr-3" width = "180px", height = "200" >
                  <div class="media-body">
                    <h5 class="mt-0">{{ blog.title }}</h5>
                    <p> {{ blog.description }} </p>
                  </div>
                </div> -->
                
                {% endfor %}

                <!-- <div class="col mb-2">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(112).webp"
                    alt="image 1" class="w-100 rounded-3">
                </div>
                <div class="col mb-2">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(107).webp"
                    alt="image 1" class="w-100 rounded-3">
                </div> -->
              </div>

              <!-- <LAYOUT 3> -->
              <!-- <div class="row g-2">
                <div class="col">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(108).webp"
                    alt="image 1" class="w-100 rounded-3">
                </div>
                <div class="col">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(114).webp"
                    alt="image 1" class="w-100 rounded-3">
                </div>
              </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
    
</template> -->