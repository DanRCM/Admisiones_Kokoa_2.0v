using UnityEngine;

public class daño : MonoBehaviour
{
    public bool isEnemy;
    private movement Movement;
    [Range(0, 3)] public int cantidadDano = 1;
    [Header("Quita vida aleatoria entre 1 y 2")]public bool aleatorio;

    private void Start()
    {
        //Al iniciar busca el componente jugador, para conseguir el script del mismo.
        GameObject player = GameObject.FindWithTag("Player");
        Movement = player.GetComponent<movement>();


    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        //Detecta si es el jugador el que entro al trigger
        if (collision.CompareTag("Player"))
        {
            //Realiza el metodo damage del script del jugador
            Movement.damage();

            //Si es aleatorio la cantidad de daño es cambiada a un numero aleatorio entre 1 y 2.
            if (aleatorio)
            {
                cantidadDano = Random.Range(1, 3);
            }

            //Se aplica el daño al script del gamaManager.
            gameManager.instance.perderVida(isEnemy,cantidadDano);
        }
    }

 
}
