export const path = 'https://demo4861279.mockable.io';

export const mocks = [
  {
    matcher: `${path}/boards/`,
    method: 'GET',
    response: [
      {
        id: 1,
        name: 'Tablero Copado',
      },
      {
        id: 2,
        name: 'Tablero Malaso',
      },
      {
        id: 3,
        name: 'Tablero Aburrido',
      },
    ],
  },
  {
    matcher: `${path}/rooms/`,
    method: 'POST',
    response: { id: 5 },
  },
];
