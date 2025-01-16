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
        yield return new WaitForSeconds(1.3f);
        Destroy(gameObject);
    }
}
