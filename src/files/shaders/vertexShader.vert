#version 330

in vec3 vertexPosition;
in vec3 vertexNormal;

uniform mat4 modelViewProjection;
uniform mat3 normalMatrix;

out vec3 normalInterp;
out vec3 vertexPositionEye;

void main()
{
    normalInterp = normalize(normalMatrix * vertexNormal);
    vertexPositionEye = (modelViewProjection * vec4(vertexPosition, 1.0)).xyz;
    gl_Position = modelViewProjection * vec4(vertexPosition, 1.0);
}