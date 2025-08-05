import { Table } from "react-bootstrap";

export default function GenericTable({ colHeaders, data, renderActions, variant }) {
    
    return (<>
        <Table striped bordered hover variant={variant} size='sm'>
            <thead>
                <tr>
                    {colHeaders.map((col) => (
                         <th key={col.key}>{col.label}</th>
                    ))}
                    {renderActions && (<th>Actions</th>)}
                </tr>
            </thead>
            <tbody>
                {data.map((item) => (
                    <tr key={item.sno}>
                        {colHeaders.map((col) => (
                            <td key={col.key}>{item[col.key]}</td>
                        ))}
                        {renderActions && (
                            <td className="d-flex gap-2">
                                {renderActions(item)}
                            </td>
                        )}
                    </tr>
                ))}
            </tbody>
        </Table>
        </>);
}