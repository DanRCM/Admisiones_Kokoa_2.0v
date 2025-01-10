using UnityEngine;

public class SpawnPoint : MonoBehaviour
{ 

    //Literal lo mismo que el chekcpoint asi que los voy a unificar si me acuerdo
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            gameManager.instance.SpawnPoint(new Vector2(transform.position.x, transform.position.y));
        }
    }
}
