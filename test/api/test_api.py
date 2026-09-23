def test_endpoint_sign_up(cliente):
    response = cliente.post("/auth/sign_up/API/V1", json={"username": "fakeusername", 
                                                 "email": "fakeemail@gmail.com", 
                                                 "password": "fakepassword"})

    assert response.status_code == 201
    assert response.json()["token_type"] == "bearer"

def test_endpoint_login(cliente):
    cliente.post("/auth/sign_up/API/V1", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/auth/login/API/V1", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

def test_endpoint_create_task(cliente):
    peyload = cliente.post("/auth/sign_up/API/V1", json={
        "username": "fakeusername", 
        "email": "fakeemail@gmail.com", 
        "password": "fakepassword"
    })   
    
    access_token = peyload.json()["access_token"]
    
    response = cliente.post("/tasks/create_task/API/V1", json={
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
    peyload_registrarse = cliente.post("/auth/sign_up/API/V1", json={
                                      "username": "fakeusername", 
                                       "email": "fakeemail@gmail.com", 
                                       "password": "fakepassword"}) 
    
    access_token = peyload_registrarse.json()["access_token"]
    cliente.post("/tasks/create_task/API/V1", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    response = cliente.get("/tasks/consult_tasks_user/API/V1", 
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert  response.status_code == 200
    assert  response.json() is not None
    assert  isinstance(response.json()["tasks"], list) 

def test_eliminar_tarea(cliente):

    peyload_registrarse = cliente.post("/auth/sign_up/API/V1", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"}) 
        
    access_token = peyload_registrarse.json()["access_token"]
    
    tarea = cliente.post("/tasks/create_task/API/V1", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              }) 
    response = cliente.delete(f"/tasks/delete_task/API/V1/{tarea.json()['id']}", headers={"Authorization": f"Bearer {access_token}" })

    assert response.status_code == 204

def test_get_tasks_by_id(cliente):
    registrarse = cliente.post("/auth/sign_up/API/V1", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"})

    access_token = registrarse.json()["access_token"]

    tarea = cliente.post("/tasks/create_task/API/V1", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    payload = cliente.get(f"/tasks/consult_user_task_by_ID/API/V1/{tarea.json()['id']}", headers={"Authorization": f"Bearer {access_token}"})

    assert payload is not None
    assert payload.status_code == 200
    assert payload.json()["name"] == "fakenombre"
    assert payload.json()["deadline"] == "2026-08-04"

def test_update_tasks(cliente):
    registrarse = cliente.post("/auth/sign_up/API/V1", json={
                                              "username": "fakeusername", 
                                               "email": "fakeemail@gmail.com", 
                                               "password": "fakepassword"})
    
    access_token = registrarse.json()["access_token"]
    
    cliente.post("/tasks/create_task/API/V1", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              })

    payload = cliente.put(f"/tasks/update_task/API/V1/{1}", json={"name": "fakenewnombre",
                                                                "deadline": "2027-09-29",
                                                                "description": "fakenewdescripcion"}, 
                                                                headers={"Authorization": f"Bearer {access_token}"})

    assert payload.json()["description"] == "fakenewdescripcion"
    assert payload is not None 
    assert payload.status_code == 200

def test_create_without_token(cliente):
    response = cliente.post("/tasks/create_task/API/V1", json={
                "name": "fakenombre",
                "deadline": "2026-08-04",
                "description": "fakedescripcion"})

    assert response.status_code == 401  

def test_get_tasks_without_token(cliente):
       response = cliente.get("/tasks/consult_tasks_user/API/V1")
       
       assert  response.status_code == 401

def test_get_non_existing_task(cliente):
    peyload_register = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })   
        
    access_token = peyload_register.json()["access_token"]
        
    cliente.post("/tasks/create_task/API/V1", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        }) 

    response = cliente.get(f"/tasks/consult_user_task_by_ID/API/V1/{9999}", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 404

def test_userA_cannot_delete_userB_task(cliente):
        usuarioA = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/tasks/create_task/API/V1", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.delete(f"/tasks/delete_task/API/V1/{tareaUsuarioB.json()['id']}", headers={"Authorization": f"Bearer {tokenusuarioA}" })

        assert response.status_code == 404    

def test_delete_non_existing_task(cliente):
      peyload_register = cliente.post("/auth/sign_up/API/V1", json={
              "username": "fakeusername", 
              "email": "fakeemail@gmail.com", 
              "password": "fakepassword"
          })   
          
      access_token = peyload_register.json()["access_token"]

      
      response = cliente.delete(f"/tasks/delete_task/API/V1/{9999999}", headers={"Authorization": f"Bearer {access_token}" })

      assert response.status_code == 404 

def test_userA_cannot_get_userB_task(cliente):
        usuarioA = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"] 

        tareaUsuarioB = cliente.post("/tasks/create_task/API/V1", json={
                    "name": "fakenombre",
                    "deadline": "2026-08-04",
                    "description": "fakedescripcion"}, headers={
                    "Authorization": f"Bearer {tokenUsuarioB}"
                })

        UsuarioA_payload = cliente.get(f"/tasks/consult_user_task_by_ID/API/V1/{tareaUsuarioB.json()['id']}", headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert UsuarioA_payload.status_code == 404 

def test_userA_cannor_update_userB_task(cliente):
        usuarioA = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/tasks/create_task/API/V1", json={
            "name": "fakenombre",
            "deadline": "2026-08-04",
            "description": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.put(f"/tasks/update_task/API/V1/{tareaUsuarioB.json()['id']}", json={"name": "fakenewnombre",
                                                                "deadline": "2027-09-29",
                                                                "description": "fakenewdescripcion"}, 
                                                                headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert response.status_code == 404

def test_singup_duplicated_username(cliente):
        cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409

def test_login_inexinting_user(cliente):
        response = cliente.post("/auth/login/API/V1", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

        assert response.status_code == 401

def test_duplicated_email(cliente):
        cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusernamenew", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409

def test_invalid_token(cliente):

     token_falso = "tokenfalsoparatestdeaopi"
     
     response = cliente.get("/tasks/consult_tasks_user/API/V1", headers={"Authorization": f"Bearer {token_falso}"})

     assert response.status_code == 401

def test_post_invalid_data(cliente):
        cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        response = cliente.post("/auth/sign_up/API/V1", json={
              "data": "invalid_data"
        })

        assert response.status_code == 422

def test_invalid_email(cliente):
        response = cliente.post("/auth/sign_up/API/V1", json={
            "username": "fakeusername", 
            "email": "invalidemail", 
            "password": "fakepassword"
        })

        assert response.status_code == 422

def test_incorrect_password(cliente):
    cliente.post("/auth/sign_up/API/V1", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/auth/login/API/V1", data={"username": "fakeusername", 
                                            "password": "contrasenaincorrecta"})

    assert response.status_code == 401

def test_non_existent_user(cliente):
    cliente.post("/auth/sign_up/API/V1", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/auth/login/API/V1", data={"username": "non_existentusername", 
                                            "password": "contrasenaincorrecta"})

    assert response.status_code == 401

def test_user_without_tasks(cliente):
    peyload = cliente.post("/auth/sign_up/API/V1", json={
        "username": "fakeusername", 
        "email": "fakeemail@gmail.com", 
        "password": "fakepassword"
    })   
    
    access_token = peyload.json()["access_token"]

    response = cliente.get("/tasks/consult_tasks_user/API/V1",
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.json()["tasks"] == []

def test_health_check(cliente):
      response = cliente.get("/health")

      assert response.json()["status"] == "ok"