using System.Collections;
using System.Runtime.CompilerServices;
using UnityEngine;

public class Monedas : MonoBehaviour
{
    //Script del comportamiento de las monedas

    //Se le aplica un valor a la moneda
    [SerializeField] private int valorMoneda = 10;
    
    //El animator de la moneda
    private Animator animator;
   
    private void Start()
    {
        //se obtiene el elemento   
        animator = GetComponent<Animator>();    
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        //Si el jugador entra en el trigger inicia una animacion, se destruye y suma puntos en el game Manager
        if (collision.CompareTag("Player"))
        {
            animator.SetTrigger("isPickup");
            AudioManager.instance.PlaySfx("cogerMoneda");
            Invoke("Destroy",0.3f);
            gameManager.instance.SumarPuntos(valorMoneda);
        }

  
    }

    private void Destroy()
    {
        Destroy(gameObject);
    }
}
