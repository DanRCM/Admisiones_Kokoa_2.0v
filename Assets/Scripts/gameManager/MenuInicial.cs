using UnityEngine;
using UnityEngine.SceneManagement;
public class MenuInicial : MonoBehaviour
{
    // Las funciones de iniciar y salir del menu principal de opciones
    public void iniciar()
    {
        gameManager.instance.cargarEscena();
    }
    public void Salir()
    {
        //Debug.log es para mostrar por consola que si se activo esta funcion
        Debug.Log("Esta saliendo");
        Application.Quit();
    }
}
