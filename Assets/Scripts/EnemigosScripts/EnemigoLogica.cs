using UnityEngine;

public class EnemigoLogica : MonoBehaviour
{
    public Animator animator;
    public GameObject enemigo;

    private void Start()
    {
        enemigo = transform.GetChild(0).gameObject;
        animator = enemigo.GetComponent<Animator>();
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            animator.SetTrigger("dead");
            AudioManager.instance.PlaySfx("poof");
            Destroy(gameObject, 0.3f);
        }
    }
}
