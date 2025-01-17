using System.Collections;
using UnityEngine;


public class doubleJump : MonoBehaviour
{
    //Este script se lo añado a las orbes azules del juego que dan un impulso hacia arriba.

    private GameObject player;
    private Rigidbody2D rb;
    [SerializeField] private float fuerzaSalto;
    private Animator animator;
    void Start()
    { 

        //Al iniciar obtiene del objeto jugador su componente rigibody encargado de las fisicas, y el animator del propio objeto
        player = GameObject.FindGameObjectWithTag("Player");
        rb = player.GetComponent<Rigidbody2D>();
        animator = GetComponent<Animator>();
    }

 
    private void OnTriggerEnter2D(Collider2D collision)
    {
        //Si entra en su trigger se inicia la animacion de recogido y se le añade un impulso hacia arriba al jugador
        animator.SetTrigger("Recogido");
        rb.linearVelocity = new Vector2(0, 0);
        rb.AddForce(Vector2.up * fuerzaSalto, ForceMode2D.Impulse);
        AudioManager.instance.PlaySfx("orbeSalto");
    }



}
