using UnityEngine;
using TMPro;
public class canvascontroller : MonoBehaviour
{
    public TextMeshProUGUI[] texto;
    public GameObject[] menusFinal;
    private void Start()
    {
    
        if (gameManager.instance.tiempoTranscurrido - gameManager.instance.puntosTotales*0.1f < gameManager.instance.tiempoGuardar)
        {
            gameManager.instance.tiempoGuardar = gameManager.instance.tiempoTranscurrido - gameManager.instance.puntosTotales*0.1f;
            Debug.Log(gameManager.instance.tiempoGuardar);
            menusFinal[0].SetActive(true);
            menusFinal[1].SetActive(false);

            int minutes = Mathf.FloorToInt(gameManager.instance.tiempoGuardar / 60);
            int seconds = Mathf.FloorToInt(gameManager.instance.tiempoGuardar % 60);
            int milliseconds = Mathf.FloorToInt((gameManager.instance.tiempoGuardar * 1000) % 1000);
            texto[0].text = $"{minutes:00}:{seconds:00}:{milliseconds:000}";

          

            

        }
        else
        {
            menusFinal[0].SetActive(false);
            menusFinal[1].SetActive(true);
            int minutes = Mathf.FloorToInt(gameManager.instance.tiempoGuardar / 60);
            int seconds = Mathf.FloorToInt(gameManager.instance.tiempoGuardar % 60);
            int milliseconds = Mathf.FloorToInt((gameManager.instance.tiempoGuardar * 1000) % 1000);
            texto[1].text = $"{minutes:00}:{seconds:00}:{milliseconds:000}";
        }



    }
    public void Salir()
    {
        gameManager.instance.fileManager.GuardarData();
        gameManager.instance.cargarEscena();
    }
}
