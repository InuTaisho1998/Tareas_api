def test_endpoint_registrarse(cliente):
    response = cliente.post("/auth/registrase/API/V1", json={"username": "fakeusername", 
                                                 "email": "fakeemail@gmail.com", 
                                                 "password": "fakepassword"})

    assert response.status_code == 201
    assert response.json()["token_type"] == "bearer"


def test_endpoint_login(cliente):
    cliente.post("/auth/registrase/API/V1", json={"username": "fakeusername", 
                                      "email": "fakeemail@gmail.com", 
                                      "password": "fakepassword"})
  
    response = cliente.post("/auth/login/API/V1", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_endpoint_crear_tarea(cliente):
    peyload = cliente.post("/auth/registrase/API/V1", json={
        "username": "fakeusername", 
        "email": "fakeemail@gmail.com", 
        "password": "fakepassword"
    })   
    
    access_token = peyload.json()["access_token"]
    
    response = cliente.post("/tareas/crear_tarea/API/V1", json={
        "nombre": "fakenombre",
        "fecha": "2026-08-04",
        "descripcion": "fakedescripcion"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    }) 
    
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["nombre"] == "fakenombre"
    


def test_dar_tareas(cliente):
    peyload_registrarse = cliente.post("/auth/registrase/API/V1", json={
                                      "username": "fakeusername", 
                                       "email": "fakeemail@gmail.com", 
                                       "password": "fakepassword"}) 
    
    access_token = peyload_registrarse.json()["access_token"]
    cliente.post("/tareas/crear_tarea/API/V1", json={
            "nombre": "fakenombre",
            "fecha": "2026-08-04",
            "descripcion": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    response = cliente.get("/tareas/consultar_tareas_usuario/API/V1", 
                           headers={"Authorization": f"Bearer {access_token}"})

    assert  response.status_code == 200
    assert  response.json() is not None
    assert  isinstance(response.json()["tareas"], list) 



def test_eliminar_tarea(cliente):

    peyload_registrarse = cliente.post("/auth/registrase/API/V1", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"}) 
        
    access_token = peyload_registrarse.json()["access_token"]
    
    tarea = cliente.post("/tareas/crear_tarea/API/V1", json={
                "nombre": "fakenombre",
                "fecha": "2026-08-04",
                "descripcion": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              }) 
    response = cliente.delete(f"/tareas/eliminar_tarea/API/V1/{tarea.json()["id"]}", headers={"Authorization": f"Bearer {access_token}" })

    assert response.status_code == 204


def test_obtener_tarea_por_id(cliente):
    registrarse = cliente.post("/auth/registrase/API/V1", json={
                                          "username": "fakeusername", 
                                           "email": "fakeemail@gmail.com", 
                                           "password": "fakepassword"})

    access_token = registrarse.json()["access_token"]

    tarea = cliente.post("/tareas/crear_tarea/API/V1", json={
            "nombre": "fakenombre",
            "fecha": "2026-08-04",
            "descripcion": "fakedescripcion"
          }, headers={
            "Authorization": f"Bearer {access_token}"
          }) 

    payload = cliente.get(f"/tareas/consultar_tarea_usuario_por_ID/API/V1/{tarea.json()["id"]}", headers={"Authorization": f"Bearer {access_token}"})

    assert payload is not None
    assert payload.status_code == 200
    assert payload.json()["nombre"] == "fakenombre"
    assert payload.json()["fecha"] == "2026-08-04"



def test_actualizar_tarea(cliente):
    registrarse = cliente.post("/auth/registrase/API/V1", json={
                                              "username": "fakeusername", 
                                               "email": "fakeemail@gmail.com", 
                                               "password": "fakepassword"})
    
    access_token = registrarse.json()["access_token"]
    
    cliente.post("/tareas/crear_tarea/API/V1", json={
                "nombre": "fakenombre",
                "fecha": "2026-08-04",
                "descripcion": "fakedescripcion"
              }, headers={
                "Authorization": f"Bearer {access_token}"
              })

    payload = cliente.put(f"/tareas/actualizar_tarea/API/V1/{1}", json={"nombre": "fakenewnombre",
                                                                "fecha": "2027-09-29",
                                                                "descripcion": "fakenewdescripcion"}, 
                                                                headers={"Authorization": f"Bearer {access_token}"})

    assert payload.json()["descripcion"] == "fakenewdescripcion"
    assert payload is not None 
    assert payload.status_code == 200


def test_crear_sin_token(cliente):
    response = cliente.post("/tareas/crear_tarea/API/V1", json={
                "nombre": "fakenombre",
                "fecha": "2026-08-04",
                "descripcion": "fakedescripcion"})

    assert response.status_code == 401  


def test_lista_sin_token(cliente):
       response = cliente.get("/tareas/consultar_tareas_usuario/API/V1")
       
       assert  response.status_code == 401


def test_obtener_tarea_inexistente(cliente):
    peyload_register = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })   
        
    access_token = peyload_register.json()["access_token"]
        
    cliente.post("/tareas/crear_tarea/API/V1", json={
            "nombre": "fakenombre",
            "fecha": "2026-08-04",
            "descripcion": "fakedescripcion"
        }, headers={
            "Authorization": f"Bearer {access_token}"
        }) 

    response = cliente.get(f"/tareas/consultar_tarea_usuario_por_ID/API/V1/{9999}", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 404

def test_usuarioA_no_eliminar_tarea_usuarioB(cliente):
        usuarioA = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/tareas/crear_tarea/API/V1", json={
            "nombre": "fakenombre",
            "fecha": "2026-08-04",
            "descripcion": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.delete(f"/tareas/eliminar_tarea/API/V1/{tareaUsuarioB.json()["id"]}", headers={"Authorization": f"Bearer {tokenusuarioA}" })

        assert response.status_code == 404

      

def test_eliminar_inexistente(cliente):
      peyload_register = cliente.post("/auth/registrase/API/V1", json={
              "username": "fakeusername", 
              "email": "fakeemail@gmail.com", 
              "password": "fakepassword"
          })   
          
      access_token = peyload_register.json()["access_token"]

      
      response = cliente.delete(f"/tareas/eliminar_tarea/API/V1/{9999999}", headers={"Authorization": f"Bearer {access_token}" })

      assert response.status_code == 404 


def test_UsuarioA_no_puede_ver_tarea_UsuarioB(cliente):
        usuarioA = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"] 

        tareaUsuarioB = cliente.post("/tareas/crear_tarea/API/V1", json={
                    "nombre": "fakenombre",
                    "fecha": "2026-08-04",
                    "descripcion": "fakedescripcion"}, headers={
                    "Authorization": f"Bearer {tokenUsuarioB}"
                })

        UsuarioA_payload = cliente.get(f"/tareas/consultar_tarea_usuario_por_ID/API/V1/{tareaUsuarioB.json()["id"]}", headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert UsuarioA_payload.status_code == 404 


def test_usuarioA_no_modificar_tarea_usuarioB(cliente):
        usuarioA = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        tokenusuarioA = usuarioA.json()["access_token"]
        
        usuarioB = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusernameusuarioB", 
            "email": "fakeemailusuarioB@gmail.com", 
            "password": "fakepassword"
        })
        tokenUsuarioB = usuarioB.json()["access_token"]

        tareaUsuarioB = cliente.post("/tareas/crear_tarea/API/V1", json={
            "nombre": "fakenombre",
            "fecha": "2026-08-04",
            "descripcion": "fakedescripcion"}, headers={
            "Authorization": f"Bearer {tokenUsuarioB}"
        })

        response = cliente.put(f"/tareas/actualizar_tarea/API/V1/{tareaUsuarioB.json()["id"]}", json={"nombre": "fakenewnombre",
                                                                "fecha": "2027-09-29",
                                                                "descripcion": "fakenewdescripcion"}, 
                                                                headers={"Authorization": f"Bearer {tokenusuarioA}"})

        assert response.status_code == 404

def test_registro_username_duplicado(cliente):
        cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409
        assert response.json()["detail"] == "Datos ya existentes"

def test_login_usuario_inexistente(cliente):
        response = cliente.post("/auth/login/API/V1", data={"username": "fakeusername", 
                                            "password": "fakepassword"})

        assert response.status_code == 401
        assert response.json()["detail"] == "Datos Incorrectos"

def test_email_duplicado(cliente):
        cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusername", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })
        
        response = cliente.post("/auth/registrase/API/V1", json={
            "username": "fakeusernamenew", 
            "email": "fakeemail@gmail.com", 
            "password": "fakepassword"
        })

        assert response.status_code == 409
        assert response.json()["detail"] == "Datos ya existentes"


def test_token_invalido(cliente):

     token_falso = "tokenfalsoparatestdeaopi"
     
     response = cliente.get("/tareas/consultar_tarea_usuario_por_ID/API/V1/1", headers={"Authorization": f"Bearer {token_falso}"})

     assert response.status_code == 401