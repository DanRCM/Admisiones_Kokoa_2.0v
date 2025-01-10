using UnityEngine;

public class BotonUtilidad : MonoBehaviour
{

    //Logica del boton dentro del juego
    [Header("Objeto a Instanciar")]//Este boton sirve para instaciar bombas por ahora
    public GameObject prefab;
    [Header("Punto donde spawneara el objeto")]
    public Transform spawn;
    private Animator animator;


    private void Start()
    {
        //Obtiene el animator
        animator = GetComponent<Animator>();    
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            //Cuando el jugador entra al trigger, inicia la animacion e instancia un prefab por ahora una bomba, en la posicion que le especifiquemos con un objeto vacio
            animator.SetBool("isPush", true);

            Instantiate(prefab, spawn.position, spawn.rotation);
        }
        
    }

    private void OnTriggerExit2D(Collider2D collision)
    {
            animator.SetBool("isPush", false);   
            //Al salir del trigger vuelve a su estado normal el boton
    }

 
}
