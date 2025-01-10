using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using TMPro;
public class botonesScript : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{

    //Este script es para la interfaz y lo tiene cada boton, lo que hace es agrandar y cambiar de color.
   [SerializeField] private Button miBoton;
    private TMP_Text text;
   [SerializeField] private Color color;
    [SerializeField] private float scaleFactor = 1.2f; // Escala al pasar el puntero
    [SerializeField] private float animationSpeed = 0.2f; // Velocidad de la animación

    private Vector3 originalScale;
    private Coroutine scaleCoroutine;

    void Start()
    {
        //Obtiene los elementos correspondientes
        text = GetComponent<TMP_Text>();
        miBoton.onClick.AddListener(OnBotonPresionado);
        originalScale = transform.localScale; 
    }

    //Cuando el puntero entra se inicia la animacion del escalado
    public void OnPointerEnter(PointerEventData eventData)
    {
        text.color = Color.yellow;
        StartScaling(originalScale * scaleFactor); 
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        text.color = Color.white;
        StartScaling(originalScale); 
    }

    void OnBotonPresionado()
    {
        text.color = color;
    }

    private void StartScaling(Vector3 targetScale)
    {
        // Detener cualquier animación previa para evitar conflictos
        if (scaleCoroutine != null)
        {
            StopCoroutine(scaleCoroutine);
        }
        scaleCoroutine = StartCoroutine(ScaleText(targetScale));
    }
   

    //Escala el texto con algo llamado lerp.
    private System.Collections.IEnumerator ScaleText(Vector3 targetScale)
    {
        Vector3 currentScale = transform.localScale;
        float progress = 0;

        while (progress < 1)
        {
            progress += Time.deltaTime / animationSpeed;
            transform.localScale = Vector3.Lerp(currentScale, targetScale, progress);
            yield return null;
        }

        transform.localScale = targetScale;
    }


    private void OnEnable()
    {
      
        if (text != null)
        {
            text.color = Color.white;
        }
    }
}
