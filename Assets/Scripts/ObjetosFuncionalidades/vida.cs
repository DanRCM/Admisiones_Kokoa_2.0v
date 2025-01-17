
using UnityEngine;

public class vida : MonoBehaviour
{
    //El script asignado a los corazones
    private Animator animator;
    private void Start()
    {
        //Obtiene el animator del objeto corazon
        animator = GetComponent<Animator>();    
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        //Si el jugador entra en su trigger detecta si se pueda ganar vida y si se gano se activa la animacion de obtenido y se destruye el objeto.
        if (collision.CompareTag("Player"))
        {
            if (gameManager.instance.ganarVida())
            {
                animator.SetBool("picked", true);
                AudioManager.instance.PlaySfx("recogerVida");
                Invoke("destruir", 0.3f);
            }
        }
    }

    private void destruir()
    {
        Destroy(gameObject);
    }
}
