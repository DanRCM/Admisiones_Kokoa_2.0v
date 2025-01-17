using System.Collections;
using UnityEngine;

public class CloseDoor : MonoBehaviour
{
    //Script para abrir la puerta
    Animator animator;
    private void Start()
    {
        animator = GetComponent<Animator>();
    }

    //Cuando entra el jugador en esta zona se inicia la cortuina para abrir la puerta.
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            StartCoroutine(abriendoPuerta());
        }
    }


    IEnumerator abriendoPuerta()
    {
        animator.SetBool("Close",true);
        AudioManager.instance.PlaySfx("openDoor");
        yield return new WaitForSeconds(1.3f);
        Destroy(gameObject);
    }
}
