export default function Home({ user }) {
  return (
    <div>
      <h1>Привет, {user.username}!</h1>
      <p>Твои группы:</p>
      {user.groups.length === 0 ? (
        <p>пока нет</p>
      ) : (
        <ul>
          {user.groups.map((name) => (
            <li key={name}>{name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
