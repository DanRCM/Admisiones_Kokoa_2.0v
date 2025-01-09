
using UnityEngine;

public class PersonajeMenu : MonoBehaviour
{
    //Esto es para que el dinosaurio que estese en el menu al moverse de un lado aparezca del otro lado de la pantalla
    public float posx;
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            collision.transform.position = new Vector2 (posx, collision.transform.position.y);
        }
    }
}
