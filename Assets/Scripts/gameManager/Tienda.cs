using UnityEngine;
using TMPro;
using UnityEngine.UI;
public class Tienda : MonoBehaviour
{
    public Button doubleJump;
    public TextMeshProUGUI cantDobleSaltos;
    public TextMeshProUGUI monedas;

    void Start()
    {
        //Al iniciar muestro el numero de monedas y muestro el numero de objetos que tengo de las dos cosas que se pueden comprar
        monedas.text = gameManager.instance.monedasUsables.ToString();


        
        cantDobleSaltos.text = gameManager.instance.dobleSaltos.ToString();
    }


    //Funcion para comprarlosSaltos.
    public void comprarSaltos()
    {
        if (gameManager.instance.getMonedasUsables() >= 200)
        {
            gameManager.instance.changeDoublejump();
            cantDobleSaltos.text = gameManager.instance.getDoublejump().ToString();
            gameManager.instance.changeMonedasUsables(200);
            monedas.text = gameManager.instance.getMonedasUsables().ToString();
        }
    }
}
