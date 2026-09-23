def test_endpoint_sign_up(cliente):
    response = cliente.post("/api/v1/auth/register", json={"username": "fakeusername", 
                                                 "email": "fakeemail@gmail.com", 
                                                 "password": "fakepassword"})

    assert response.status_code == 201
    assert response.json()["token_type"] == "bearer"

def test_endpoint_login(cliente):
    cliente.post("/api/v1/auth/register", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/api/v1/auth/login", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

def test_endpoint_create_task(cliente):
    peyload = cliente.post("/api/v1/auth/register", json={
        "username": "fakeusername", 
        "email": "fakeemail@gmail.com", 
        "password": "fakepassword"
    })   
    
    access_token = peyload.json()["access_token"]
    
    response = cliente.post("/api/v1/tasks", json={
        "name": "fakenombre",
        "deadline": "2026-08-04",
        "description": "fakedescripcion"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["name"] == "fakenombre"


def test_get_tasks(cliente):
    peyload_registrarse = cliente.post("/api/v1/auth/register", json={
                                      "username": "fakeusername", 
                                       "email": "fakeemail@gmail.com", 
                                       "password": "fakepassword"}) 
    
    access_token = peyload_registrarse.json()["access_token"]
    cliente.post("/api/v1/tasks", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    response = cliente.get("/api/v1/tasks", 
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert  response.status_code == 200
    assert  response.json() is not None
    assert  isinstance(response.json()["tasks"], list) 

def test_eliminar_tarea(cliente):

    peyload_registrarse = cliente.post("/api/v1/auth/register", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"}) 
        
    access_token = peyload_registrarse.json()["access_token"]
    
    tarea = cliente.post("/api/v1/tasks", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              }) 
    response = cliente.delete(f"/api/v1/tasks/{tarea.json()['id']}", headers={"Authorization": f"Bearer {access_token}" })

    assert response.status_code == 204

def test_get_tasks_by_id(cliente):
    registrarse = cliente.post("/api/v1/auth/register", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"})

    access_token = registrarse.json()["access_token"]

    tarea = cliente.post("/api/v1/tasks", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    payload = cliente.get(f"/api/v1/tasks/{tarea.json()['id']}", headers={"Authorization": f"Bearer {access_token}"})
    
    assert payload is not None
    assert payload.status_code == 200
    assert payload.json()["name"] == "fakenombre"
    assert payload.json()["deadline"] == "2026-08-04"

def test_update_tasks(cliente):
    registrarse = cliente.post("/api/v1/auth/register", json={
                                              "username": "fakeusername", 
                                               "email": "fakeemail@gmail.com", 
                                               "password": "fakepassword"})
    
    access_token = registrarse.json()["access_token"]
    
    tarea = cliente.post("/api/v1/tasks", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              })

    payload = cliente.put(f"/api/v1/tasks/{tarea.json()['id']}",json={
                "name": "fakenewnombre",
                "deadline": "2027-08-04",
                "description": "fakenewdescripcion"}, headers={
                "Authorization": f"Bearer {access_token}"})
    print({"sub": payload.json()})
    
    assert payload.json()["description"] == "fakenewdescripcion"
    assert payload is not None 
    assert payload.status_code == 200

def test_create_without_token(cliente):
    response = cliente.post("/api/v1/tasks", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"})

    assert response.status_code == 401  

def test_get_tasks_without_token(cliente):
       response = cliente.get("/api/v1/tasks")
       
       assert  response.status_code == 401

def test_get_non_existing_task(cliente):
    peyload_register = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })   
        
    access_token = peyload_register.json()["access_token"]
        
    cliente.post("/api/v1/tasks", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        }) 

    response = cliente.get(f"/api/v1/tasks{9999}", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 404

def test_userA_cannot_delete_userB_task(cliente):
        usuarioA = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/api/v1/tasks", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.delete(f"/api/v1/tasks/{tareaUsuarioB.json()['id']}", headers={"Authorization": f"Bearer {tokenusuarioA}" })

        assert response.status_code == 404    

def test_delete_non_existing_task(cliente):
      peyload_register = cliente.post("/api/v1/auth/register", json={
              "username": "fakeusername", 
              "email": "fakeemail@gmail.com", 
              "password": "fakepassword"
          })   
          
      access_token = peyload_register.json()["access_token"]

      
      response = cliente.delete(f"/api/v1/tasks/{9999999}", headers={"Authorization": f"Bearer {access_token}" })

      assert response.status_code == 404 

def test_userA_cannot_get_userB_task(cliente):
        usuarioA = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"] 

        tareaUsuarioB = cliente.post("/api/v1/tasks", json={
                    "name": "fakenombre",
                    "deadline": "2026-08-04",
                    "description": "fakedescripcion"}, headers={
                    "Authorization": f"Bearer {tokenUsuarioB}"
                })

        UsuarioA_payload = cliente.get(f"/api/v1/tasks{tareaUsuarioB.json()['id']}", headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert UsuarioA_payload.status_code == 404 

def test_userA_cannor_update_userB_task(cliente):
        usuarioA = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/api/v1/tasks", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.put(f"/api/v1/tasks{tareaUsuarioB.json()['id']}", json={"name": "fakenewnombre",
                                                                "deadline": "2027-09-29",
                                                                "description": "fakenewdescripcion"}, 
                                                                headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert response.status_code == 404

def test_singup_duplicated_username(cliente):
        cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409

def test_login_inexinting_user(cliente):
        response = cliente.post("/api/v1/auth/login", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

        assert response.status_code == 401

def test_duplicated_email(cliente):
        cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusernamenew", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409

def test_invalid_token(cliente):

     token_falso = "tokenfalsoparatestdeaopi"
     
     response = cliente.get("/api/v1/tasks", headers={"Authorization": f"Bearer {token_falso}"})

     assert response.status_code == 401

def test_post_invalid_data(cliente):
        cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        response = cliente.post("/api/v1/auth/register", json={
              "data": "invalid_data"
        })

        assert response.status_code == 422

def test_invalid_email(cliente):
        response = cliente.post("/api/v1/auth/register", json={
            "username": "fakeusername", 
            "email": "invalidemail", 
            "password": "fakepassword"
        })

        assert response.status_code == 422

def test_incorrect_password(cliente):
    cliente.post("/api/v1/auth/register", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/api/v1/auth/login", data={"username": "fakeusername", 
                                            "password": "contrasenaincorrecta"})

    assert response.status_code == 401

def test_non_existent_user(cliente):
    cliente.post("/api/v1/auth/register", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/api/v1/auth/login", data={"username": "non_existentusername", 
                                            "password": "contrasenaincorrecta"})

    assert response.status_code == 401

def test_user_without_tasks(cliente):
    peyload = cliente.post("/api/v1/auth/register", json={
        "username": "fakeusername", 
        "email": "fakeemail@gmail.com", 
        "password": "fakepassword"
    })   
    
    access_token = peyload.json()["access_token"]

    response = cliente.get("/api/v1/tasks",
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.json()["tasks"] == []

def test_health_check(cliente):
      response = cliente.get("/health")

      assert response.json()["status"] == "ok"