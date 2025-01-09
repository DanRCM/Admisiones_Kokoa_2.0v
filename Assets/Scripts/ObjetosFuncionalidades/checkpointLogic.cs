using UnityEngine;

public class checkpointLogic : MonoBehaviour
{
    // Script del checkpoint, el del spawnpoint es muy similar probablemente los fusione y ponga una condicion de si es spawnpoint o checkpoint
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            //Guarda en el game manager el ultimo checkpoint
            gameManager.instance.lastCheckpoint(new Vector2 (transform.position.x,transform.position.y));
        }
    }
}
